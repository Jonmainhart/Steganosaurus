# Unit Tests

This folder contains unit test for the Steganosaurus application. The tests are intended to provide suitable coverage for the main functionality of the application. Some features are not well-suited to automated testing and therefore have not been included.

## Requirements

The automated tests for this project are written for the Pytest framework. Pytest can be installed via pip using the following:

`python3 -m pip install Pytest`

## Running Tests

1. Go to the `../Steganosaurus/` directory in your terminal. Note that the exact location depends on where you installed the application.
2. Enter `pytest steganosaurus/tests/test.py steganosaurus/tests/stegoTest.py -v` into your terminal and press enter.
There are currently 30 tests to run, so it may take a while. In some cases, testing can run for several minutes. When testing is complete, your terminal will display something similar to the following:

![screenshot](https://github.com/Jonmainhart/cmsc495_final/blob/66b8922d5058ea675f9955d88131efd232750ab8/Steganosaurus/steganosaurus/tests/terminal.png)

## Troubleshooting

Most issues with successfully executing tests are due to the tester being in the wrong directory or from the tester changing the folder structure of the project and not accounting for those changes in the test file or the application files. Double check you are in the (big S) Steganosaurus folder and try to run the tests again as described above. Consult the [Pytest documentation](https://docs.pytest.org/en/7.1.x/) if you are still unable to get the tests running.
