"""Colour for the verdict in Code Runner's Output panel.

That panel cannot show a terminal's colours; it is coloured by a grammar, like a source file. The grammar
lives in vscode/verdict-colours, a VS Code extension with no code in it. This packs it and hands it to VS Code.
The colours themselves are in .vscode/settings.json, under editor.tokenColorCustomizations.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from .catalog import ROOT

SOURCE = ROOT / "vscode" / "verdict-colours"

_CONTENT_TYPES = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension=".json" ContentType="application/json"/>
<Default Extension=".vsixmanifest" ContentType="text/xml"/>
</Types>
"""

_MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
<Metadata>
<Identity Language="en-US" Id="{name}" Version="{version}" Publisher="{publisher}"/>
<DisplayName>{displayName}</DisplayName>
<Description xml:space="preserve">{description}</Description>
<Categories>Other</Categories>
<Properties><Property Id="Microsoft.VisualStudio.Code.Engine" Value="{engine}"/></Properties>
</Metadata>
<Installation><InstallationTarget Id="Microsoft.VisualStudio.Code"/></Installation>
<Dependencies/>
<Assets><Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true"/></Assets>
</PackageManifest>
"""


def pack(target: Path) -> Path:
    """The extension as a .vsix, the zip VS Code installs from."""
    package = json.loads((SOURCE / "package.json").read_text())
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", _CONTENT_TYPES)
        archive.writestr("extension.vsixmanifest", _MANIFEST.format(engine=package["engines"]["vscode"], **package))
        for path in sorted(SOURCE.rglob("*")):
            if path.is_file():
                archive.write(path, f"extension/{path.relative_to(SOURCE).as_posix()}")
    return target


def install() -> bool:
    code = shutil.which("code")
    if code is None:
        return False
    with tempfile.TemporaryDirectory() as folder:
        vsix = pack(Path(folder) / "leet-verdict-colours.vsix")
        return subprocess.run([code, "--install-extension", str(vsix), "--force"], capture_output=True).returncode == 0
