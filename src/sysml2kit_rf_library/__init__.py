"""SysML v2 model library for antenna/RF systems engineering.

Ships the RFVocabulary/RFParts/RFRequirements/RFAnalyses packages plus a
worked 28 GHz satcom-terminal example, as committed interchange JSON loadable
through sysml2kit. ``_build.py`` is the authoritative source; the files under
``models/`` are generated from it.
"""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from sysml2kit.model import Model

try:
    __version__ = version("sysml2kit-rf-library")
except PackageNotFoundError:  # running from a source tree without an install
    __version__ = "0.0.0.dev0"

#: Available model names -> interchange file stem.
MODELS = {
    "rf-library": "rf_library",
    "satcom-terminal-t3001": "satcom_terminal_t3001",
}


def models_dir() -> Path:
    """Return the directory holding the packaged model files."""
    return Path(__file__).parent / "models"


def load_model(name: str = "rf-library") -> Model:
    """Load a packaged model by name (see ``MODELS``)."""
    from sysml2kit.interchange import model_from_json

    if name not in MODELS:
        raise KeyError(f"unknown model {name!r}; available: {sorted(MODELS)}")
    return model_from_json(models_dir() / "interchange" / f"{MODELS[name]}.json")


__all__ = ["MODELS", "__version__", "load_model", "models_dir"]
