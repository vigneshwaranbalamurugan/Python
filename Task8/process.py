import pandas as pd
from email_alert import send_email_alert

class ProcessSensorData:
    def __init__(self):
        self.df = pd.DataFrame()

    def processdata(self, data):
        self.df = pd.concat(
            [self.df, pd.DataFrame([data])],
        )

        if len(self.df) > 5:
            self.df = self.df.tail(5)

        result = {}

        for column in ["temperature", "vibration"]:
            series = self.df[column]
            mean = float(series.mean())
            std = float(series.std())
            value = float(series.iloc[-1])

            if std == 0:
                z_score = 0.0
            else:
                z_score = float((value - mean) / std)

            alert_flag = bool(abs(z_score) > 1.5 or value > 45)
            if alert_flag:
                send_email_alert(column, value, data["timestamp"])
            result[column] = {
                "value": value,
                "moving_avg": round(mean, 2),
                "z_score": round(z_score, 2),
                "alert": alert_flag
            }
            
        result["timestamp"] = str(data["timestamp"])
        return result