import pytest

from datetime import datetime, timezone
from model_mommy import mommy
from django.core.management import call_command
from usaspending_api.submissions.models import DABSSubmissionWindowSchedule

SCHEDULE_FILE = "usaspending_api/data/testing_data/test_dabs_submission_window_schedule.csv"

FUTURE_DATE = datetime(9999, 12, 31, tzinfo=timezone.utc)
CURRENT_REVEAL_DATE = datetime(2000, 1, 1, tzinfo=timezone.utc)


@pytest.mark.django_db
def test_schedule_is_updated(client):
    mommy.make(
        "submissions.DABSSubmissionWindowSchedule",
        id=2020121,
        submission_reveal_date="2020-12-23",
        certification_due_date="2020-12-23",
        submission_fiscal_year=99,
    )

    call_command("load_dabs_submission_window_schedule", file=SCHEDULE_FILE)
    schedule = DABSSubmissionWindowSchedule.objects.get(id=2020121)

    assert schedule.submission_fiscal_year == 2020

    # Submission Reveal Date should not be updated
    assert schedule.submission_reveal_date == datetime(2020, 12, 23, tzinfo=timezone.utc)


@pytest.mark.django_db
def test_future_schedule_is_updated(client):
    mommy.make(
        "submissions.DABSSubmissionWindowSchedule",
        id=2777121,
        submission_reveal_date="2076-12-23",
        certification_due_date="2076-12-23",
        submission_fiscal_year=2076,
    )

    call_command("load_dabs_submission_window_schedule", file=SCHEDULE_FILE)
    schedule = DABSSubmissionWindowSchedule.objects.get(id=2777121)

    assert schedule.submission_fiscal_year == 2777

    # Submission Reveal Date is updated
    assert schedule.submission_reveal_date == datetime(9999, 12, 31, tzinfo=timezone.utc)


@pytest.mark.django_db
def test_non_matching_schedule_is_removed(client):
    mommy.make(
        "submissions.DABSSubmissionWindowSchedule",
        id=2010121,
        submission_reveal_date="2010-12-23",
        certification_due_date="2010-12-23",
        submission_fiscal_year=2010,
    )

    call_command("load_dabs_submission_window_schedule", file=SCHEDULE_FILE)
    schedule_count = DABSSubmissionWindowSchedule.objects.all().filter(id=2010121).count()
    assert schedule_count == 0


@pytest.mark.django_db
def test_schedule_is_created(client):
    call_command("load_dabs_submission_window_schedule", file=SCHEDULE_FILE)
    schedule = DABSSubmissionWindowSchedule.objects.get(id=2888121)

    # Record exists and Submission Reveal Date is set to future date
    assert schedule.submission_reveal_date == FUTURE_DATE


@pytest.mark.django_db
def test_quarter_vs_month(client):
    # Month Schedules
    mommy.make("submissions.DABSSubmissionWindowSchedule", id=10, submission_reveal_date=CURRENT_REVEAL_DATE)
    mommy.make("submissions.DABSSubmissionWindowSchedule", id=11, submission_reveal_date=CURRENT_REVEAL_DATE)

    # Quarter Schedule
    mommy.make("submissions.DABSSubmissionWindowSchedule", id=20, submission_reveal_date=CURRENT_REVEAL_DATE)
    mommy.make("submissions.DABSSubmissionWindowSchedule", id=21, submission_reveal_date=CURRENT_REVEAL_DATE)

    call_command("load_dabs_submission_window_schedule", file=SCHEDULE_FILE)

    month_schedule_unrevealed = DABSSubmissionWindowSchedule.objects.get(id=10)
    month_schedule_revealed = DABSSubmissionWindowSchedule.objects.get(id=11)

    quarter_schedule_revealed = DABSSubmissionWindowSchedule.objects.get(id=20)
    quarter_schedule_unrevealed = DABSSubmissionWindowSchedule.objects.get(id=21)

    assert month_schedule_revealed.submission_reveal_date == CURRENT_REVEAL_DATE
    assert month_schedule_unrevealed.submission_reveal_date == FUTURE_DATE

    assert quarter_schedule_revealed.submission_reveal_date == CURRENT_REVEAL_DATE
    assert quarter_schedule_unrevealed.submission_reveal_date == FUTURE_DATE
