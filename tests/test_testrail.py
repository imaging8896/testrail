def test_testrailutil(testdir, test_cfg):
    testdir.makeconftest("""
        import pytest
        from pytest_testrailutil.plugin import *
    """)

    # You may need to change case ids
    testdir.makepyfile("""
        import pytest
        
        @pytest.fixture
        def f_a():
            raise Exception("Setup failure.")
            return 

        @pytest.mark.testrail("C45673")
        def test_setup_failed(f_a):
            assert True
            
        @pytest.mark.testrail("C31877")
        @pytest.mark.skip(reason="skippppppppppp~")
        def test_skip(f_a):
            assert True
            
        @pytest.fixture
        def f_b():
            yield
            raise Exception("Teardown failure.")
        
        @pytest.mark.testrail("C45640")
        def test_teardown_failed(f_b):
            assert True

        @pytest.mark.testrail("C47861")
        def test_pass():
            assert True

        @pytest.mark.testrail("C47866")
        def test_failed():
            assert False
            
        def test_no_tag_pass():
            assert True
            
        def test_no_tag_failed():
            assert False
    """)

    result = testdir.runpytest("-s", "--testrail=" + test_cfg, "--user=plugintest")
    result.assert_outcomes(passed=3, failed=2, error=2, skipped=1)
