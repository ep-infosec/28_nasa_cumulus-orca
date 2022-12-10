import logging
import unittest

import testtools

import test_packages


class TracingStreamResult(testtools.StreamResult):
    """
    Properly captures test results for later reporting.
    Without this, the default StreamResult class does not raise an error when a test fails.
    See https://testtools.readthedocs.io/en/latest/api.html for more details.
    """

    def __init__(self):
        self.test_results = {}

    def status(self, *args, **kwargs) -> None:
        test_id = kwargs["test_id"]
        test_status = kwargs["test_status"]
        if test_status == "fail":
            logging.error(f"Test failed: {test_id}")

        self.test_results[test_id] = kwargs["test_status"]


def run_tests() -> None:
    """
    Runs all tests in linked modules concurrently.
    Raises:
        Exception: Thrown once processing of all tests concludes if any test failed.
    """
    logging.getLogger().setLevel(logging.INFO)
    suite = unittest.TestLoader().loadTestsFromModule(test_packages)
    concurrent_suite = testtools.ConcurrentStreamTestSuite(
        lambda: ((case, None) for case in suite)
    )
    result = TracingStreamResult()  # testtools.StreamResult()
    result.startTestRun()
    concurrent_suite.run(result)
    result.stopTestRun()

    logging.info(f"Checking results on {len(result.test_results)} tests...")
    failed_tests = []
    for test_name in result.test_results:
        if result.test_results[test_name] == "success":
            logging.info(f"{test_name} passed")
        else:
            failed_tests.append(test_name)

    if any(failed_tests):
        raise Exception(f"Tests failed: {failed_tests}")

    logging.info("Tests passed.")


if __name__ == "__main__":
    run_tests()
