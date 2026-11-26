"""The lab copies of the artifacts jobs must follow their cloud jobs."""

from pathlib import Path

import pytest

from sdcm.utils.lint.jenkins_parser import parse_jenkinsfile

ARTIFACTS_DIR = Path(__file__).parents[2] / "jenkins-pipelines" / "oss" / "artifacts"
LAB_OSES = [
    "rocky9",
    "centos9-web",
    "centos9-selinux",
    "debian12",
    "debian13",
    "ubuntu2204-web",
    "ubuntu2404",
    "ubuntu2604",
]


@pytest.mark.parametrize("os_name", [pytest.param(name, id=name) for name in LAB_OSES])
def test_lab_job_follows_its_cloud_job(os_name):
    """A lab job runs the config of its cloud job plus the minicloud overlays, on the repo that scylla-pkg sends."""
    cloud = parse_jenkinsfile(ARTIFACTS_DIR / f"artifacts-{os_name}.jenkinsfile")
    lab = parse_jenkinsfile(ARTIFACTS_DIR / f"artifacts-{os_name}-minicloud.jenkinsfile")
    overlay = f"configurations/minicloud/{cloud.params['backend']}.yaml"

    assert lab.test_config == cloud.test_config + ["configurations/minicloud.yaml", overlay]
    assert lab.params["backend"] == cloud.params["backend"]
    assert "scylla_version" not in lab.params
