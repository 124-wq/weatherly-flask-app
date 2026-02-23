if weather:
            record = WeatherRecord(
                city=weather["city"],  
                temperature=weather["temperature"],
                description=weather["description"],
                humidity=weather["humidity"],
                latitude=weather["latitude"],
                longitude=weather["longitude"]
            )
