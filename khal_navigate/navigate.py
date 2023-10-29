import calendar as cl

from khal.cli_utils import multi_calendar_option, build_collection, multi_calendar_select
from khal.exceptions import FatalError
from khal import controllers

import click
import datetime as dt


# returns a couple of strings based on the date format, the first one is the first day of the indicated week number month number and year
# the second is the final day of the week
def parsing_daterange(
    dateformat,
    week_number:int,
    month_number:int,
    year_number:int,
):
    assert week_number is not None
    assert month_number is not None
    assert year_number is not None


    first_date=''
    second_date=''

    if week_number is not None and month_number is not None and year_number is not None:

        first_day_week = dt.date(year_number, month_number, 1).isoweekday()
        init = 7-first_day_week+1
        if week_number == 1:
            date1 = dt.datetime(year_number,month_number,1)
            first_date = date1.strftime(dateformat)
            date2 = dt.datetime(year_number,month_number,init)
            second_date = date2.strftime(dateformat)
        if week_number == 2:
            date1 = dt.datetime(year_number,month_number,init+1)
            first_date = date1.strftime(dateformat)
            date2 = dt.datetime(year_number,month_number,init+7)
            second_date = date2.strftime(dateformat)
        if week_number == 3:
            date1 = dt.datetime(year_number,month_number,init+8)
            first_date = date1.strftime(dateformat)
            date2 = dt.datetime(year_number,month_number,init+14)
            second_date = date2.strftime(dateformat)
        if week_number == 4:
            date1 = dt.datetime(year_number,month_number,init+15)
            first_date = date1.strftime(dateformat)
            date2 = dt.datetime(year_number,month_number,init+21)
            second_date = date2.strftime(dateformat)
        if week_number == 5:
            date1 = dt.datetime(year_number,month_number,init+22)
            first_date = date1.strftime(dateformat)
            if month_number != 12:
                tdelta = (dt.date(year_number,month_number+1,1)-dt.date(year_number,month_number,2))
            if month_number == 12:
                tdelta = (dt.date(year_number+1,1,1)-dt.date(year_number,month_number,2))
            date2 = dt.datetime(year_number,month_number,1) + tdelta
            second_date = date2.strftime(dateformat)
        daterange = first_date,second_date
        return daterange

@click.command("navigate")
@multi_calendar_option
@click.option('--agenda_format', '-f',
              help=('The format of the events.'))
@click.option('--week', '-w' ,help=('The number of the week: 1,2,3,4'))
@click.option('--month', '-m',help=('The number of the month: 1,2..12'))
@click.option('--year', '-y' ,help=('The year'))

@click.option('--day-format', '-df',
              help=('The format of the day line.'))
@click.option('--once', '-o', is_flag=True,
              help=('Print each event only once '
                    '(even if it is repeated or spans multiple days).')
              )

@click.option('--notstarted', help=('Print only events that have not started.'),
              is_flag=True)
@click.pass_context
def knavigate(ctx, include_calendar, exclude_calendar,week, month,year, agenda_format, notstarted, day_format, once):
    """List all events navigating by week, month or year."""
    try:
        dateformat = ctx.obj['conf']['locale']['dateformat']
        cal = cl.Calendar(0)
       # in the case we only gave the week
        if week is not None and month is None and year is None:
            week_number = int(week)
            # if the given week is between 1 and 5, it list the events of the week of the current month
            if 1 <= week_number <=5:
                month_number = dt.datetime.today().month
                year_number = dt.datetime.today().year
                dateRange = controllers.parsing_daterange(dateformat,week_number,month_number,year_number)
            # if the given week n is superior to 5, the week is considered as the nth week of the current year
            if  5 < week_number < 54 :
                year_number = dt.datetime.today().year
                a = week_number * 7
                strt_date = dt.date(year_number, 1, 1)
                date1 = strt_date + dt.timedelta(a -7)
                date2 = strt_date + dt.timedelta(a - 1)
                first_date = date1.strftime(dateformat)
                second_date = date2.strftime(dateformat)
                dateRange = first_date, second_date
            # week must be inferior to 54
            if week_number >= 54:
                raise click.BadParameter('The week option has to be inferior to 54'
                'The value 1 stands for the first week of the current month, the value 2 stands for the second week and so on...'
                'if the week chosen has a value superior to five, this will be applied to the current year; The value 6 stands'
                'for the sixth week of the current year and so on...'
                )
        # in the case we gave week and year
        if week is not None and month is None and year is not None :
            week_number = int(week)
            year_number = int(year)
            init = 0
            for i in cal.itermonthdays(year_number,1) :
                if i != 0 :
                    break
                init += 1
            if (week_number < 52 and init > 1) or (week_number < 53 and init == 0) :
                a = week_number * 7
                if (init == 0) :
                    strt_date = dt.date(year_number, 1, 1)
                else :
                    strt_date = dt.date(year_number, 1, 8 - init)
                date1 = strt_date + dt.timedelta(a -7)
                date2 = strt_date + dt.timedelta(a - 1)
                first_date = date1.strftime(dateformat)
                second_date = date2.strftime(dateformat)
                dateRange = first_date, second_date
            elif (week_number >= 53 and init > 1) or (week_number >= 54 and init == 0) :
                raise click.BadParameter('The week option has to have a value of 1,2,3,4...53'
                'The value 1 stands for the first week of the chosen year, the value 2 stands for the second week and so on...'
                )
            else :
                first_date = dt.date(year_number, 12, 31 - init+1).strftime(dateformat)
                second_date = dt.date(year_number + 1, 1, 8 - init -1).strftime(dateformat)
                dateRange = first_date, second_date

         #in the case we only gave month
        if week is None and month is not None and year is None:
            month_number = int(month)
            if 1 <= month_number <= 12:
                year_number = dt.datetime.today().year
                if month_number != 12 :
                    tdelta = (dt.date(year_number,month_number+1,1)-dt.date(year_number,month_number,2))
                if month_number == 12 :
                    tdelta = (dt.date(year_number+1,1,1)-dt.date(year_number,month_number,2))
                first_date = (dt.datetime(year_number,month_number,1)).strftime(dateformat)
                date2 = dt.datetime(year_number,month_number,1) + tdelta
                second_date = date2.strftime(dateformat)
                dateRange = first_date, second_date
            else:
                raise click.BadParameter('The month option has to have a value of 1,2...12, '
                'The value 1 stands for the first month...The value 2 stands for the last month'
                )
        # in the case we only gave year
        if week is None and month is None and year is not None:
            year_number = int(year)
            first_date = (dt.datetime(year_number,1,1)).strftime(dateformat)
            tdelta = (dt.date(year_number+1,1,1)-dt.date(year_number,12,2))
            date2 = dt.datetime(year_number,12,1) + tdelta
            second_date = date2.strftime(dateformat)
            dateRange = first_date, second_date

        #in the case we gave week, month and year
        if week is not None and month is not None and year is not None:
            week_number = int(week)
            month_number = int(month)
            year_number = int(year)
            try :
                weeksOfMonth = cal.monthdatescalendar(year_number, month_number)
                week = weeksOfMonth[week_number-1]
                first_date = week[0]
                second_date = week[6]
                for (index,day) in enumerate(week) :
                    if day.month == month_number - 1 or day.year == year_number - 1 :
                        first_date = week[index + 1]
                    if day.month == month_number + 1 or day.year == year_number + 1 :
                        second_date = week[index - 1]
                        break
                dateRange = first_date.strftime(dateformat), second_date.strftime(dateformat)

            except :
                raise click.BadParameter('The week option has to have a value of 1,2,3,4 or 5, '
                    'The value 1 stands for the first week, the value 2 stands for the second week and so on...'
                'The month option has to have a value of 1,2...12,'
                'The value 1 stands for the first month...The value 2 stands for the last month'
                )

        event_column = controllers.khal_list(
            build_collection(
                ctx.obj['conf'],
                multi_calendar_select(ctx, include_calendar, exclude_calendar)
            ),
            agenda_format=agenda_format,
            day_format=day_format,
            daterange=dateRange,
            once=once,
            notstarted=notstarted,
            conf=ctx.obj['conf'],
            env={"calendars": ctx.obj['conf']['calendars']}
        )
        if event_column:
            click.echo('\n'.join(event_column))

        else:
            logger.debug('No events found')

    except FatalError as error:
        logger.debug(error, exc_info=True)
        logger.fatal(error)
        sys.exit(1)
