import io
import json
from typing import Tuple, Dict, List, Union, Any
from google.cloud import vision
from google.cloud.vision import enums
from google.protobuf.json_format import MessageToJson


class ApiVision:
    """
    Wrapper around Google Cloud Vision Python library
    """

    LIKELYHOOD_NAME = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )
    default_features = [
        {"type": enums.Feature.Type.SAFE_SEARCH_DETECTION},
        {"type": enums.Feature.Type.LABEL_DETECTION},
        {"type": enums.Feature.Type.LANDMARK_DETECTION},
    ]

    def __init__(self, photo: Union[str, io.BytesIO]) -> None:
        """
        Initialize image object regardless of URI or BytesIO object is passed
        """

        self.client = vision.ImageAnnotatorClient()
        if isinstance(photo, io.BytesIO):
            self.image = vision.types.Image(content=photo.getvalue())
        else:
            self.image = vision.types.Image()
            self.image.source.image_uri = photo

    def detect_safe_search(self) -> Dict[str, str]:
        """
        Detects unsafe features in the image
        """

        safe_response = self.client.safe_search_detection(
            image=self.image).safe_search_annotation
        safe_search = {
            "adult": self.LIKELYHOOD_NAME[safe_response.adult],
            "violence": self.LIKELYHOOD_NAME[safe_response.violence],
            "racy": self.LIKELYHOOD_NAME[safe_response.racy],
        }
        return safe_search

    def detect_landmarks(self) -> Dict[str, Tuple[Any, Any]]:
        """
        Detects landmarks in the image
        """

        landmark_response = self.client.landmark_detection(
            image=self.image).landmark_annotations
        return {
            landmark.description: (
                location.lat_lng.latitude, location.lat_lng.longitude
                )
            for landmark in landmark_response
            for location in landmark.locations
        }

    def detect_labels(self) -> List[str]:
        """
        Detects labels of the image
        """

        label_response = self.client.label_detection(
            image=self.image).label_annotations
        labels = [label.description for label in label_response]
        return labels

    def batch_annotate_image(
                self, *features_to_detect: enums.Feature.Type
            ) -> vision.types.BatchAnnotateImagesResponse:
        """
        Detect several features in one request. By default makes annotations
        for "SAFE_SEARCH", "LABEL" and "LANDMARK".
        Example of usage with arguments:
        batch_annotate_image(enums.Feature.Type.SAFE_SEARCH_DETECTION)
        """

        requests = [
            {"image": self.image,
             "features": [
                {"type": feature} for feature in features_to_detect]
                or self.default_features}
        ]
        response = self.client.batch_annotate_images(requests)
        return self.format_response(response)

    @staticmethod
    def format_response(
            response: vision.types.BatchAnnotateImagesResponse
            ) -> Dict[Any, Any]:

        resp = json.loads(MessageToJson(response))["responses"][0]
        formatted_response = {}
        if "landmarkAnnotations" in resp:
            formatted_response["landmarks"] = [
                {
                    landmark["description"]: [
                        (location["latLng"]["latitude"],
                         location["latLng"]["longitude"])
                        for location in landmark["locations"]
                    ]
                    for landmark in resp["landmarkAnnotations"]
                }
            ]
        if "labelAnnotations" in resp:
            formatted_response["labels"] = [
                label["description"] for label in resp["labelAnnotations"]
            ]
        if "safeSearchAnnotation" in resp:
            formatted_response["safe_search"] = {
                feature: resp["safeSearchAnnotation"][feature]
                for feature in resp["safeSearchAnnotation"]
                }
        return formatted_response
