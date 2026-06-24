import requests


ML_API_URL = "http://localhost:8001/predict"


def predict_stress(features):



    try:

        response = requests.post(
            ML_API_URL,
            json=features,
            timeout=10

        )


        response.raise_for_status()
        result = response.json()


        if ("stress_probability" not in result):

            raise Exception("ML API did not return stress_probability")
        return result


    except requests.exceptions.Timeout:


        raise Exception("ML API timeout" )


    except requests.exceptions.ConnectionError:


        raise Exception("Cannot connect to ML API")


    except Exception as e:


        raise Exception(f"ML API Error: {e}")