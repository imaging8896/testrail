def test_testrailutil(testdir, test_cfg):
    testdir.makeconftest("""
        import pytest
        from pytest_testrailutil.plugin import *
    """)

    # You may need to change case ids
    testdir.makepyfile("""
        import pytest
        
        @pytest.fixture
        def f_normal():
            print "f_normal setup"
            yield
            print "f_normal teardown" 
            
        @pytest.fixture
        def f_setup_failed():
            print "f_setup_failed setup"
            raise Exception("Setup failure.")
            return 
            
        @pytest.fixture
        def f_teardown_failed():
            print "f_teardown_failed setup"
            yield
            print "f_teardown_failed teardown"
            raise Exception("Teardown failure.")
            
            
        # Skipped
            
        @pytest.mark.testrail("C33356")
        @pytest.mark.skip(reason="test_skip_success~")
        def test_skip_success():
            print "test_skip_success test"
            assert True
            
        @pytest.mark.testrail("C66439")
        @pytest.mark.skip(reason="test_skip_fixture_success~")
        def test_skip_fixture_success(f_normal):
            print "test_skip_fixture_success test"
            assert True
            
        @pytest.mark.testrail("C31877")
        @pytest.mark.skip(reason="test_skip_setup_failed~")
        def test_skip_setup_failed(f_setup_failed):
            print "test_skip_setup_failed test"
            assert True
            
        @pytest.mark.testrail("C45673")
        @pytest.mark.skip(reason="test_skip_setup_failed~")
        def test_skip_teardow_failed(f_teardown_failed):
            print "test_skip_teardow_failed test"
            assert True 
            
        
        # Setup failed
            
        @pytest.mark.testrail("C45640")
        def test_success_setup_failed(f_setup_failed):
            print "test_success_setup_failed test"
            assert True
            
        @pytest.mark.testrail("C45636")
        def test_failed_setup_failed(f_setup_failed):
            print "test_failed_setup_failed test"
            assert False
    
            
        # Teardown failed
        
        @pytest.mark.testrail("C61391")
        def test_success_teardown_failed(f_teardown_failed):
            print "test_success_teardown_failed test"
            assert True
            
        @pytest.mark.testrail("C62278")
        def test_failed_teardown_failed(f_teardown_failed):
            print "test_failed_teardown_failed test"
            assert False
            
        
        # Setup failed teardown failed
        
        @pytest.mark.testrail("C62279")
        def test_success_setup_teardown_failed(f_setup_failed, f_teardown_failed):
            print "test_success_setup_teardown_failed test"
            assert True 
            
        @pytest.mark.testrail("C66423")
        def test_failed_setup_teardown_failed(f_setup_failed, f_teardown_failed):
            print "test_failed_setup_teardown_failed test"
            assert False
            
        
        # Setup teardown success

        @pytest.mark.testrail("C66424")
        def test_pass():
            print "test_pass test"
            assert True
            
        @pytest.mark.testrail("C47861")
        def test_pass_fixture(f_normal):
            print "test_pass_fixture test"
            assert True

        @pytest.mark.testrail("C47866")
        def test_failed():
            print "test_failed test"
            assert False
            
        @pytest.mark.testrail("C47867")
        def test_failed_fixture(f_normal):
            print "test_failed_fixture test"
            assert False
            
        
        # No tag
            
        def test_no_tag_pass():
            print "test_no_tag_pass test"
            assert True
            
        def test_no_tag_pass_fixture(f_normal):
            print "test_no_tag_pass_fixture test"
            assert True
            
        def test_no_tag_failed():
            print "test_no_tag_failed test"
            assert False
            
        def test_no_tag_failed_fixture(f_normal):
            print "test_no_tag_failed_fixture test"
            assert False
    """)

    result = testdir.runpytest("-s", "--testrail=" + test_cfg, "--user=plugintest")
    result.assert_outcomes(passed=5, failed=5, error=6, skipped=4)
