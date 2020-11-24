# This is runner script
# User should be able to pass environment, browser name, page(s) arguments
# Give mechanism to get corresponding arguments within tests

import argparse
from datetime import datetime
import os
import json
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from multiprocessing import Pool
from string import Template

import requests

parser = argparse.ArgumentParser(description='Typing run')
parser.add_argument('--env', type=str, default='live', help='Set the environment in which tests will be run', choices=['new', 'live'])
parser.add_argument('--page', '-p', nargs='+', help='run specific class tests', choices=['teacher-signup',
                                                                    'teacher-classes',
                                                                    'teacher-curriculum',
                                                                    'teacher-order',
                                                                    'teacher-assignments'])
parser.add_argument('--throughput', help='simulate internet connection speed')
parser.add_argument('--group', type=str, default='', help='run specific group tests')
parser.add_argument('--case', type=str, default='', help='Input page')
parser.add_argument('--thread_count', '-t', default=None, help=' run tests in parallel')
parser.add_argument('--browser', '-b', nargs='+', help='specify the browser in which tests will be run, please note that you can specify multiple browsers', default=['chrome'],
                    choices=['chrome', 'safari', 'firefox', 'edge'])
parser.add_argument('--to_email', type=str, default=None, help='to send email report to specified email address')
parser.add_argument('--from_email', type=str, default='harut@instigatemobile.com', help='specify sender email')
parser.add_argument('--password', type=str, default='Mal!bu123', help='specify sender password')
parser.add_argument('--smtp_host', type=str, default='mail.instigatemobile.com', help='specify SMTP host')
parser.add_argument('--smtp_port', default='587', help='specify SMTP port')
parser.add_argument('--send_slack', default=False)
parser.add_argument('--slack_hook',
                    default='https://hooks.slack.com/services/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', help='specify the Incoming Webhooks url')
args = parser.parse_args()

url_add = {"new": "new", "live": "www"}

base_url = 'https://{}.typing.com'.format(url_add[args.env])

os.environ["ENV"] = args.env
os.environ["URL"] = base_url

if args.throughput is not None:
    os.environ['THROUGHPUT'] = args.throughput

print(f'Running the tests using {args.browser} parallel threads')

bashCommand = f"pytest -s --verbose " \
              "--allure-link-pattern=test_case:https://docs.google.com/spreadsheets/d/1P54UmzfJggGuXzZV4zMfZ1I6Isv8P5Ac0a_F_u1Deyg/edit?ts=5fb694ba#gid=763370721&range={} --allure-link-pattern=issue:https://docs.google.com/spreadsheets/d/1P54UmzfJggGuXzZV4zMfZ1I6Isv8P5Ac0a_F_u1Deyg/edit?ts=5fb694ba#gid=886796583&range={}"
if args.page is not None:
    for page in args.page:
        bashCommand += f" tests/{page}_page_test.py"
else:
    bashCommand +=" tests/"
if args.thread_count is not None:
    bashCommand += f" -n {args.thread_count}"
if args.group:
    bashCommand += f' -m {args.group}'
if args.case:
    bashCommand = f' -k {args.case}'


def send_slack_report(passed, failed, skipped, error, browser, platform, duration):
    color = '#e51c23' if failed > 0 or error > 0 else '#259b24'
    emoji = ':thumbsdown:' if failed > 0 or error > 0 else ':thumbsup:'
    total = passed + failed + skipped + error
    now = datetime.now()
    report = {
        "text": "Test Automation Report | " + f"{browser.upper()} | {now.strftime('%d/%m/%Y %H:%M:%S')}",
        "icon_emoji": f"{emoji}",
        "attachments": [
            {
                "color": f"{color}",
                "text": f"PLATFORM: {platform}\n"
                        f"DURATION: {duration}\n"
                        f"TOTAL TESTS: {total}\n"
                        f"TEST STATUS: Passed={passed} Failed={failed} Skipped={skipped} Error={error}",
                "attachment_type": "default"
            }
        ]
    }
    json_params_encoded = json.dumps(report)
    requests.post(url=args.slack_hook, data=json_params_encoded, headers={"Content-type": "application/json"})


def send_email_report(passed, fail, skip, error, browser, platform, duration):
    status = 'FAILED' if fail > 0 or error > 0 else 'PASSED'
    status_color = 'red' if status == 'FAILED' else 'green'
    now = datetime.now()
    total = passed + fail + skip + error

    msg = MIMEMultipart('alternative')
    to = args.to_email
    me = args.from_email
    pswd = args.password
    msg[
        'Subject'] = f"Test Automation Report | {passed}/{total} | {browser.upper()} |{now.strftime('%d/%m/%Y %H:%M:%S')}"
    msg['From'] = me
    msg['To'] = to
    html = """
    <html>
<head>

   <title>Tutsplus Email Newsletter</title>
   <style type="text/css">
    #appInfo, #report, .title {
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  table-layout: fixed;
  width: 50%;
}

#appInfo td, #report td {
  border: 1px solid #ddd;
  padding: 8px;
  color: #003e77;
}

#appInfo tr td:nth-child(1){
  font-weight: bold;
}

#appInfo tr:hover {background-color: #ddd;}

.title {
    color: #003e77;
}

#report tr:nth-child(1) td:nth-child(1) {
  font-weight: bold;
  color:green;
}

#report tr:nth-child(2) td:nth-child(1) {
  font-weight: bold;
  color:red;
}

#report tr:nth-child(3) td:nth-child(1) {
  font-weight: bold;
  color:gray;
}

#report tr:nth-child(4) {
  font-weight: bold;
  background-color: #e1e3e1;
}
   </style>
</head>
<body>
<h1><b><font style="color:$ST_COLOR;">$STATUS</font></b></h1>
      <h3 class="title"><b>Details</b></h3>
      <table id="appInfo">
        <tbody>
          <tr>
            <td>Environment</td>
            <td><a href="$URL"
                moz-do-not-send="true">$ENVIRONMENT</a></td>
          </tr>
          <tr>
            <td>BROWSER</td>
            <td>$BROWSER</td>
          </tr>
          <tr>
            <td>PLATFORM</td>
            <td>$PLATFORM</td>
          </tr>
          <tr>
            <td>DURATION</td>
            <td>$DURATION</td>
          </tr>

        </tbody>
      </table>
      <h3 class="title"><b>Execution results</b></h3>
      <table id="report">
        <tbody>
          <tr>
            <td style="color:green;">PASSED</td>
            <td style="color:green;">$PASSED</td>
          </tr>
          <tr id="fail">
            <td style="color:red;">FAILED</td>
            <td style="color:red;">$FAILED</td>
          </tr>
          <tr>
            <td style="color:blue;">SKIPPED</td>
            <td style="color:blue;">$SKIPPED</td>
          </tr>
          <tr id='fail'>
            <td style="color:red;">ERROR</td>
            <td style="color:red;">$ERROR</td>
          </tr>
          <tr>
            <td>TOTAL</td>
            <td>$TOTAL</td>
          </tr>
        </tbody>
      </table>
      <p class="title"><b>Typing: </b><a
          href="https://typing.com"
          moz-do-not-send="true">https://typing.com</a></p>
    </div>
</body>
</html>

    """
    html = Template(html).substitute(PLATFORM=platform, ST_COLOR=status_color,
                                     STATUS=status, BROWSER=browser.upper(), FAILED=fail, PASSED=passed,
                                     SKIPPED=skip, ERROR=error, TOTAL=total, ENVIRONMENT=base_url,
                                     URL=base_url, DURATION=duration)
    part2 = MIMEText(html, "html")

    msg.attach(part2)
    s = smtplib.SMTP(args.smtp_host, args.smtp_port)

    s.starttls()

    s.login(me, pswd)

    s.sendmail(me, [to], msg.as_string())


def run_command(browser: str):
    global bashCommand
    os.environ["BROWSER"] = browser
    bashCommand += f' --alluredir=results_{browser} --json-report --json-report-summary --json-report-file={browser}_report.json'
    print(bashCommand)
    print(subprocess.call(bashCommand.split(' ')))
    subprocess.call(f"allure generate results_{browser} --clean -o allure-reports_for_{browser}".split(' '))

    if args.to_email is not None or args.send_slack:
        with open(f'{browser}_report.json') as json_report:
            data = json.load(json_report)
            duration = f"{round(data['duration'])} seconds"
            platform = data['environment']['Platform']
            summary = data['summary']
            passed = summary['passed'] if 'passed' in summary else 0
            failed = summary['failed'] if 'failed' in summary else 0
            error = summary['error'] if 'error' in summary else 0
            skipped = summary['skipped'] if 'skipped' in summary else 0

            if args.send_slack:
                send_slack_report(passed, failed, skipped, error, browser, platform, duration)
            if args.to_email is not None:
                send_email_report(passed, failed, skipped, error, browser, platform, duration)

if __name__ == '__main__':
    pool = Pool()
    pool.map(run_command, args.browser)
    pool.close()
    pool.join()

print(f'1.Used {args.thread_count} threads to run this tests'
      f'\n2.Used {args.browser} browsers fot this tests')
