import io
from google.cloud.vision import enums

from vision_api import ApiVision


TEST_URI = "gs://cloud-samples-data/vision/landmark/st_basils.jpeg"


def test_vision_api_stream() -> None:
    with open("./tests/test_image_paris.jpeg", "rb") as image:
        TEST_FILE_STREAM = io.BytesIO(image.read())
        assert isinstance(TEST_FILE_STREAM, io.BytesIO)

        image_stream = ApiVision(TEST_FILE_STREAM)
        safe_search = image_stream.detect_safe_search()
        assert safe_search["adult"]
        assert safe_search["violence"]
        assert safe_search["racy"]
        labels = image_stream.detect_labels()
        assert labels
        response = image_stream.batch_annotate_image(
            enums.Feature.Type.LANDMARK_DETECTION,
            enums.Feature.Type.LABEL_DETECTION
        )
        assert response
        assert "Landmark" and "Tower" in response["labels"]
        assert response["landmarks"][0]["Eiffel Tower"]

        response_full = image_stream.batch_annotate_image()
        assert response_full
        assert response_full["safe_search"]["violence"] == "VERY_UNLIKELY"
        assert response_full["safe_search"]["adult"] == "VERY_UNLIKELY"


def test_vision_api_remote_image() -> None:
    image_gc = ApiVision(TEST_URI)
    explicit_content = image_gc.detect_safe_search()
    assert explicit_content["adult"]
    assert explicit_content["violence"]
    assert explicit_content["racy"]
    landmarks = image_gc.detect_landmarks()
    assert landmarks
    labels = image_gc.detect_labels()
    assert labels


if __name__ == "__main__":
    test_vision_api_stream()
    test_vision_api_remote_image()
