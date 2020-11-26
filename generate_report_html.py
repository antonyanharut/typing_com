import threading

from string import Template


class GenerateHTMLReport():
    lock = threading.RLock()
    html_head = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css"
              integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
        <link rel="shortcut icon" type="image/x-icon" href="favicon.ico"/>
    
    </head>
    
    <body>
    <blockquote class="blockquote text-center">
        <h1 class="mb-0" style="-webkit-text-stroke: 4px black;">Test Automation Reports</h1>
        <footer class="badge badge-primary text-wrap">$BROWSERS</footer>
    </blockquote>
    <div class="container-fluid rounded-circle">"""

    def append_title(self, browsers):
        self.lock.acquire()
        self.html_head = Template(self.html_head).substitute(BROWSERS=', '.join(browsers))
        self.lock.release()

    def append(self, browser, platform, duration, passed, failed, skipped, error):
        self.lock.acquire()
        self.html_head += Template("""    
    
    <a href="allure-reports_for_$BROWSER/index.html">
        <div class="container shadow-lg p-3 mb-5 bg-white rounded">
            <img class="rounded-circle position-absolute" src="../assets/$BROWSER.png">
            <h3 class="text-center">Results for $BROWSER browser</h3>
            <table class="table table-borderless">
                <thead>
                <tr>
                    <th scope="col">Platform</th>
                    <th scope="col">Test run duration</th>
                    <th scope="col">Passed</th>
                    <th scope="col">Failed</th>
                    <th scope="col">Skipped</th>
                    <th scope="col">Error</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <th scope="row">$PLATFORM</th>
                    <td>$DURATION</td>
                    <td>$PASSED</td>
                    <td>$FAILED</td>
                    <td>$SKIPPED</td>
                    <td>$ERROR</td>
                </tr>
                </tbody>
            </table>
        </div>
        </a>""").substitute(BROWSER=browser, PLATFORM=platform, DURATION=duration,
                            PASSED=passed,
                            FAILED=failed, SKIPPED=skipped, ERROR=error)
        self.lock.release()

    def generate(self):
        self.lock.acquire()
        self.html_head += """
        
        </div>
    
    
    </body>
    </html>
        """
        report = open("reports/index.html", "w")
        report.write(self.html_head)
        report.close()
        self.lock.release()
