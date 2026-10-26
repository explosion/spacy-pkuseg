import os
import subprocess
import sys

import spacy_pkuseg


def test_import_creates_no_temp_dir():
    # Importing used to create a TemporaryDirectory that was never cleaned
    # up, which emitted a ResourceWarning at interpreter exit
    result = subprocess.run(
        [
            sys.executable,
            "-W",
            "error",
            "-c",
            "import spacy_pkuseg; "
            "assert spacy_pkuseg.config._tmp_dir is None",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_train_and_segment(tmp_path):
    sents = ["我 爱 北京 天安门", "北京 是 中国 的 首都", "我 爱 中国"] * 5
    train_file = tmp_path / "train.txt"
    train_file.write_text("\n".join(sents) + "\n", encoding="utf-8")
    model_dir = tmp_path / "model"
    spacy_pkuseg.train(str(train_file), str(train_file), str(model_dir), train_iter=2)
    assert (model_dir / "features.msgpack").exists()
    assert (model_dir / "weights.npz").exists()
    seg = spacy_pkuseg.pkuseg(model_name=str(model_dir))
    assert "".join(seg.cut("我爱北京")) == "我爱北京"
    temp_dir = spacy_pkuseg.config.tempFile
    assert os.path.isdir(temp_dir)
