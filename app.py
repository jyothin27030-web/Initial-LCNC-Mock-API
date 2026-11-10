from fastapi import FastAPI

app = FastAPI(title="LCNC Mock API")


@app.get("/")
def root():
    return {
        "success": True,
        "message": "LCNC Mock API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "UP"
    }


@app.get("/api/v1/datapoints")
def datapoints():

    return {
        "datapoints": [
            {
                "id": "V44593161Battery",
                "displayName": "V44593161Battery",
                "dataType": "BOOLEAN",
                "states": [
                    {
                        "value": 0,
                        "text": "False"
                    },
                    {
                        "value": 1,
                        "text": "True"
                    }
                ]
            },
            {
                "id": "V44593162Battery",
                "displayName": "V44593162Battery",
                "dataType": "ENUM",
                "states": [
                    {
                        "value": 0,
                        "text": "Morning"
                    },
                    {
                        "value": 12,
                        "text": "Noon"
                    },
                    {
                        "value": 18,
                        "text": "Evening"
                    },
                    {
                        "value": 24,
                        "text": "Night"
                    }
                ]
            },
            {
                "id": "V72003271Battery",
                "displayName": "V72003271Battery",
                "dataType": "FLOAT",
                "unit": "V"
            }
        ]
    }


@app.post("/api/v1/telemetry")
def telemetry(payload: dict):

    point_id = payload.get("pointId")
    value = payload.get("value")

    # TC_MP_008
    if not point_id:
        return {
            "errorCode": "MISSING_ATTRIBUTE",
            "message": "pointId is required"
        }

    # TC_MP_012
    if value is None:
        return {
            "errorCode": "NULL_VALUE",
            "message": "Telemetry value cannot be null"
        }

    # Analog Point
    if point_id == "V72003271Battery":

        # TC_MP_007
        if not isinstance(value, (int, float)):
            return {
                "errorCode": "INVALID_DATA_TYPE",
                "message": "Analog point expects numeric value"
            }

        return {
            "success": True,
            "pointType": "ANALOG",
            "value": round(float(value), 6)
        }

    # Binary Point
    elif point_id == "V44593161Battery":

        if value in [0, False]:
            return {
                "success": True,
                "pointType": "BINARY",
                "state": "False"
            }

        if value in [1, True]:
            return {
                "success": True,
                "pointType": "BINARY",
                "state": "True"
            }

        return {
            "errorCode": "INVALID_BINARY_STATE",
            "message": "Binary point accepts only 0,1,true,false"
        }

    # Multi-State Point
    elif point_id == "V44593162Battery":

        mapping = {
            0: "Morning",
            12: "Noon",
            18: "Evening",
            24: "Night"
        }

        if value not in mapping:
            return {
                "errorCode": "UNKNOWN_STATE",
                "message": "ENUM value not defined"
            }

        return {
            "success": True,
            "pointType": "MULTISTATE",
            "state": mapping[value]
        }

    return {
        "errorCode": "UNKNOWN_POINT",
        "message": "Point not found"
    }