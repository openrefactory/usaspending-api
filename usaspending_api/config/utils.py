from typing import Any, Dict, Callable, TypeVar

from pydantic import BaseSettings
from pydantic.fields import ModelField

# Placeholder sentinel value indicating a config var that is expected to be overridden in a runtime-env-specific
# config declaration. If this value emerges, it has not yet been set in the runtime env config and must be.
ENV_SPECIFIC_OVERRIDE = "?ENV_SPECIFIC_OVERRIDE?"

# Placeholder sentinel value indicating a config var that is expected to be overridden from a runtime env to
# accommodate a var value that is specific to an individual developer's local environment setup.
# If this value emerges, it has not yet been set in the user's config (e.g. .env file) and and must be.
USER_SPECIFIC_OVERRIDE = "?USER_SPECIFIC_OVERRIDE?"

# Placeholder sentinel value indicating that a default should NOT be provided for a field, because its default value
# is provided by a factory function (likely one provided within a function annotated with @pydantic.validator)
FACTORY_PROVIDED_VALUE = "?FACTORY_PROVIDED_VALUE?"

CONFIG_VAR_PLACEHOLDERS = [ENV_SPECIFIC_OVERRIDE, USER_SPECIFIC_OVERRIDE, FACTORY_PROVIDED_VALUE]

TBaseSettings = TypeVar("TBaseSettings", bound=BaseSettings)


def eval_default_factory(
    config_class: TBaseSettings,
    assigned_or_sourced_value: Any,
    configured_vars: Dict[str, Any],
    config_var: ModelField,
    factory_func: Callable,
):
    """A delegate function that acts as a default factory to produce/derive (or transform) a config var value

    NOTE: This functions's signature follows that of pydantic validator functions, because it is to be delegated to
    from validator functions.

    Args:
        config_class (TBaseSettings): The class inheriting from pydantic.BaseSettings who is being instantiated. It
            is NOT (necessarily) the class on which this config_var (or its validator) resides.

        config_var (ModelField): The pydantic setting aka field aka configuration variable for which to
            factory-derive a value

        assigned_or_sourced_value (Any): The value that pydantic found for this config var. It could be coming from
            an assignment, or from a config source, like environment variables.

        configured_vars (Dict[str, Any]): Dictionary of configuration variables that have been seen/processed (IN
            ORDER) by pydantic already. Note: due to the fact that validators are processed in the order of
            ModelFields in the model being seen, this dictionary may not be inclusive of ALL fields in the model (of
            all configuration variables), simply because they haven't been seen/processed yet.

        factory_func (Callable): A lambda or callable function passed in
            which will be invoked to produce a value for the field. The provided factory function is assumed to be a
            closure, enclosing variable values it needs in its scoped defniition so they don't need to be passed in.
            See Example below for a no-param lambda closure

        Example:
            >>> @validator("MY_COMPOSED_FIELD")
            >>> def _MY_COMPOSED_FIELD(cls, v, values, field: ModelField):
            >>>     def factory_func():
            >>>         return values["MY_FIELD_1"] + ":" + values["MY_FIELD_2"]
            >>>     return eval_default_factory(cls, v, values, field, factory_func)
    """
    # This "default_value" is the value that this field was declared with in python code. Note if it is
    #  overridden in a subclass, this will be the value assigned to the field in the subclass, which could differ
    #  from any 'default' value assigned in a super class.
    default_value = config_var.default

    # Get any parent config class fields, to determine if this field may be overriding it
    overridable_config_base_classes = [
        bc for bc in config_class.__bases__ if issubclass(bc, BaseSettings) and "__fields__" in dir(bc)
    ]
    overridable_config_fields = {k for bc in overridable_config_base_classes for k in bc.__fields__.keys()}
    is_override = config_var.name in overridable_config_fields

    if not is_override and default_value is not None and default_value not in CONFIG_VAR_PLACEHOLDERS:
        raise ValueError(
            "This field, which is tied to a default-factory-based validator, must have its default value set to None,"
            "or to one of the CONFIG_VAR_PLACEHOLDERS. This is so that when a value is sourced or assigned "
            "elsewhere for this field, it can easily be identified as a non-default value, and will take "
            "precedence as the new value."
        )

    # if (
    #     is_override
    #     # A non-placeholder default_value was provided somewhere (instantiated class, or parent class)
    #     and default_value is not None
    #     and default_value not in CONFIG_VAR_PLACEHOLDERS
    #     and config_var.name not in declared_config_fields  # not a field (re)declared on the instantiated class
    # ):
    #     raise TypeError(
    #         "You may be 'overriding' a parent class config var in a subclass by way of a validator, "
    #         "without re-delcaring that config var in the subclass. If so, redeclare it above its validator in the "
    #         "subclass as:\n\t"
    #         "CONFIG_VAR = FACTORY_PROVIDED_VALUE"
    #     )

    if assigned_or_sourced_value and assigned_or_sourced_value not in CONFIG_VAR_PLACEHOLDERS:
        # The value of this field is being explicitly set in some source (initializer param, env var, etc.)
        # So honor it and don't use the default below
        return assigned_or_sourced_value

    if is_override and default_value not in CONFIG_VAR_PLACEHOLDERS:
        return default_value  # the value set on the overriding subclass is next in line for precedence

    # Otherwise let this validator be the field's default factory
    # The provided factory function is assumed to be a closure, enclosing variable values it needs in its scoped
    # definition so they don't need to be passed in.
    # NOTE: pydantic orders annotated (even fields annotated with their typing Type, like field_name: str)
    #       BEFORE non-annotated fields. And the values dict ONLY has field values for fields it has seen,
    #       seeing them IN ORDER. So if the provided factory function references OTHER fields to produced the
    #       value for the field in question, AND the field in question is annotated, the other fields must be
    #       [type] annotated as well for their values to be accessible, or an error will raise.
    return factory_func()