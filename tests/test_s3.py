from pathlib import Path

from moto import mock_s3


def test_create_list_buckets(botree_session, botree_test_bucket):
    """Creation and bucket list methods."""
    with mock_s3():
        botree_session.s3.create_bucket(botree_test_bucket)
        buckets = botree_session.s3.list_buckets()
        assert buckets == [botree_test_bucket]


def test_listobj_upload_download(botree_session, botree_test_bucket, text_file):
    """List objects, upload and download methods."""
    with mock_s3():
        botree_session.s3.create_bucket(botree_test_bucket)

        botree_session.s3.bucket(botree_test_bucket).upload(text_file, text_file.name)

        files = botree_session.s3.bucket(botree_test_bucket).list_objects()

        assert files == [text_file.name]

        download_temp_file = Path(text_file.parent, "download_temp_file.txt")

        botree_session.s3.bucket(botree_test_bucket).download(
            text_file.name, download_temp_file
        )

        assert Path(download_temp_file).is_file()


def test_copy_object(botree_session, botree_test_bucket, text_file):
    """Copy object method."""
    with mock_s3():
        other_botree_test_bucket = "other-botree-test-bucket"

        botree_session.s3.create_bucket(botree_test_bucket)

        botree_session.s3.create_bucket(other_botree_test_bucket)

        uploaded_file_path = Path(text_file.name)

        botree_session.s3.bucket(other_botree_test_bucket).upload(
            text_file, uploaded_file_path
        )

        botree_session.s3.bucket(botree_test_bucket).copy(
            uploaded_file_path, uploaded_file_path, source_bucket=other_botree_test_bucket
        )

        files = botree_session.s3.bucket(botree_test_bucket).list_objects()
        assert files == [uploaded_file_path.name]
