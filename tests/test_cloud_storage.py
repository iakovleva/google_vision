import io
from cloud_storage import upload_blob, delete_blob


def test_cloud_storage() -> None:
    with open("./tests/test_image_paris.jpeg", "rb") as image:
        TEST_FILE_STREAM = io.BytesIO(image.read())
        filename = "paris_1"
        assert isinstance(TEST_FILE_STREAM, io.BytesIO)
        assert upload_blob(TEST_FILE_STREAM, filename=filename)
        delete_blob(filename)


if __name__ == "__main__":
    test_cloud_storage()
