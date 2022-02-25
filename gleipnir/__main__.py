"""
Gleipnir is a program with graphical user interface for visualizing the results
of modeling the absorption of radiation by stellar and planetary matter.
Compatible file format for parsing (commonly named as "AbsorpPlot.dat"):
    nR <int>
    nZ <int>
    dr <float>
    dz <float>
    r0 <float>
    z0 <float>
    V1 <float>
    V2 <float>
    dV <float>
    Incl <float>
    ENA <float>
    Coeff <float>
    arrays
    AbsPlot
    <float values from 0.0 to 1.0 with size (nR + 1) x (nZ + 1),
     each value separated by space>
    <empty string>

Development notes:
    Application architecture based on "MVP Passive View" pattern with some
    extensions (model <-> presenter <-> view bindings) due to Qt's signals/slots
    abilities.
    Model is described at model/model.py file.
    View is described at ui/.../view.py files (corresponding to each widget).
    Presenter is described at ui/.../presenter.py files (corresponding to each
    widget, if needed).

Author: Artem Shepelin
License: GPLv3
Repository: https://github.com/deverte/gleipnir
"""

import sys

from PyQt6.QtWidgets import QApplication

import gleipnir.ui.presenter as presenter
import gleipnir.ui.view as view
import gleipnir.model.model as model


def main():
    app = QApplication(sys.argv)

    app_model = model.Model()
    app_view = view.MainWindowView()
    app_presenter = presenter.MainWindowPresenter(app_model, app_view)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()