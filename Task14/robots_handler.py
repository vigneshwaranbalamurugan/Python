import urllib.robotparser

class RobotsHandler:
    def __init__(self, base_url):
        self.rp = urllib.robotparser.RobotFileParser()
        robots_url = base_url + "/robots.txt"
        self.rp.set_url(robots_url)
        self.rp.read()

    def allowed(self, url):
        return self.rp.can_fetch("*", url)