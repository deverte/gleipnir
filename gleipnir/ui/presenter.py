"""
Presenter is a module that connects model and view. It contains main application
presenter, that initializes view's initial values and binds data between model
and view. It also contains some helper functions that helps to transform data.

Development notes:
    1) You can initialize initial widget's value at
    `MainWindowPresenter._set_view_initial_values`.
    2) You can bind widget's value changes to a model using signals/slots at
    `MainWindowPresenter._bind_view_to_model` function.
    3) You can bind model's value changes to a view using signals/slots at
    `MainWindowPresenter._bind_model_to_view` function.
    4) You can add additional validators and helper data transformer methods.

Author: Artem Shepelin
License: GPLv3
"""

import os
import sys

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QColorDialog
from PyQt6.QtWidgets import QErrorMessage
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QMessageBox

from gleipnir.__init__ import __version__
from gleipnir.ui.plot_widget.view import PlotWidget


class MainWindowPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self._set_view_initial_values()
        self._bind_view_to_model()
        self._bind_model_to_view()


    def _action_about(self):
        QMessageBox.about(self.view, "About Gleipnir",
            "Gleipnir is a program for visualizing the results of modeling the "
            "absorption of radiation by stellar and planetary matter.\n"
            "\n"
            f"Version: {__version__}\n"
            "Author: Artem Shepelin\n"
            "License: GPLv3\n"
            "Repository: https://github.com/deverte/gleipnir")


    def _action_open_as_data(self):
        try:
            file_name = QFileDialog.getOpenFileName(
                self.view, "Open File", "",
                "Data Files (*.dat);;All Files (*.*)")[0]
            if file_name:
                self.model.data = file_name
        except FileNotFoundError:
            QErrorMessage(self.view).showMessage(
                f"File {self.model.input_file.value} does not exist.")
        except Exception:
            QErrorMessage(self.view).showMessage(
                f"File {self.model.input_file.value} has an incompatible format.")


    def _action_open_data(self):
        try:
            self.model.data = self.model.input_file.value
        except FileNotFoundError:
            QErrorMessage(self.view).showMessage(
                f"File {self.model.input_file.value} does not exist.")
        except Exception:
            QErrorMessage(self.view).showMessage(
                f"File {self.model.input_file.value} has an incompatible format.")


    def _action_save_as_data(self):
        if not self.model.data.value:
            QErrorMessage(self.view).showMessage("Nothing to save.")
            return
        ftypes = [f"{val} (*.{key})" for key, val
                  in self.view.plotWidget.get_supported_filetypes().items()]
        save_file_dialog = QFileDialog(self.view)
        file_path = os.path.split(self.model.input_file.value)[0]
        if os.path.exists(file_path):
            save_file_dialog.setDirectory(file_path)
        save_file_dialog.setNameFilter(";;".join(ftypes))
        save_file_dialog.selectNameFilter(ftypes[5]) # png
        if save_file_dialog.exec():
            file_name = save_file_dialog.selectedFiles()[0]
            if file_name:
                try:
                    self.model.data_write(file_name,
                                          self.view.plotWidget.figure)
                except:
                    QErrorMessage(self.view).showMessage(
                        f"Can't save file {file_name}.")


    def _action_save_data(self):
        if not self.model.data.value:
            QErrorMessage(self.view).showMessage("Nothing to save.")
            return
        file_path = os.path.split(self.model.input_file.value)[0]
        if not os.path.exists(file_path):
            QErrorMessage(self.view).showMessage(
                f"Path {file_path} does not exist.")
            return
        if not self.model.output_file.value:
            QErrorMessage(self.view).showMessage(
                f"Please, configure output file name.")
            return
        try:
            self.model.data_write(self.model.output_file.value,
                                  self.view.plotWidget.figure)
        except:
            QErrorMessage(self.view).showMessage(
                f"Can't save file {self.model.output_file.value}.")


    def _bind_model_to_view(self):
        self.model.axes_color.changed.connect(self.view.plotWidget.setAxesColor)
        self.model.axes_labels_color.changed.connect(self.view.plotWidget.setAxesLabelsColor)
        self.model.background_color.changed.connect(self.view.plotWidget.setBackgroundColor)
        self.model.center_lines_color.changed.connect(self.view.plotWidget.setCenterLinesColor)
        self.model.colormap.changed.connect(self.view.plotWidget.setColormap)
        self.model.data.changed.connect(self.view.plotWidget.setData)
        self.model.dpi.changed.connect(self.view.plotWidget.setDpi)
        self.model.frame_color.changed.connect(self.view.plotWidget.setFrameColor)
        self.model.input_file.changed.connect(self.view.inputFileLineEdit.setText)
        self.model.is_background_transparent.changed.connect(self.view.plotWidget.setIsBackgroundTransparent)
        self.model.is_center_lines_displayed.changed.connect(self.view.plotWidget.setIsCenterLinesDisplayed)
        self.model.is_show_frame.changed.connect(self.view.plotWidget.setIsShowFrame)
        self.model.output_file.changed.connect(self.view.outputFileLineEdit.setText)
        self.model.ticks_color.changed.connect(self.view.plotWidget.setTicksColor)
        self.model.title.changed.connect(self.view.plotWidget.setTitle)
        self.model.title_color.changed.connect(self.view.plotWidget.setTitleColor)
        self.model.v_max.changed.connect(self.view.plotWidget.setVMax)
        self.model.v_min.changed.connect(self.view.plotWidget.setVMin)
        self.model.x_axis_name.changed.connect(self.view.plotWidget.setXAxisName)
        self.model.y_axis_name.changed.connect(self.view.plotWidget.setYAxisName)


    def _bind_view_to_model(self):
        self.view.actionAbout.triggered.connect(self._action_about)
        self.view.actionOpen.triggered.connect(self._action_open_as_data)
        self.view.actionQuit.triggered.connect(lambda : sys.exit())
        self.view.actionSave.triggered.connect(self._action_save_data)
        self.view.actionSave_As.triggered.connect(self._action_save_as_data)
        self.view.axesColorColorButton.colorChanged.connect(self.model.axes_color.setValue)
        self.view.axesLabelsColorColorButton.colorChanged.connect(self.model.axes_labels_color.setValue)
        self.view.backgroundColorColorButton.colorChanged.connect(self.model.background_color.setValue)
        self.view.centerLinesColorColorButton.colorChanged.connect(self.model.center_lines_color.setValue)
        self.view.colormapComboBox.currentTextChanged.connect(self.model.colormap.setValue)
        self.view.dpiSpinBox.valueChanged.connect(self.model.dpi.setValue)
        self.view.frameColorColorButton.colorChanged.connect(self.model.frame_color.setValue)
        self.view.inputFileLineEdit.dropped.connect(self.model.input_file.setValue)
        self.view.inputFileLineEdit.editingFinished.connect(lambda : self.model.input_file.setValue(self.view.inputFileLineEdit.text()))
        self.view.isBackgroundTransparentCheckBox.stateChanged.connect(self.model.is_background_transparent.setValue)
        self.view.isCenterLinesDisplayedCheckBox.stateChanged.connect(self.model.is_center_lines_displayed.setValue)
        self.view.isShowFrameCheckBox.stateChanged.connect(self.model.is_show_frame.setValue)
        self.view.openAsFilePushButton.clicked.connect(self._action_open_as_data)
        self.view.openFilePushButton.clicked.connect(self._action_open_data)
        self.view.outputFileLineEdit.editingFinished.connect(lambda : self.model.output_file.setValue(self.view.outputFileLineEdit.text()))
        self.view.saveAsPushButton.clicked.connect(self._action_save_as_data)
        self.view.savePushButton.clicked.connect(self._action_save_data)
        self.view.ticksColorColorButton.colorChanged.connect(self.model.ticks_color.setValue)
        self.view.titleColorColorButton.colorChanged.connect(self.model.title_color.setValue)
        self.view.titleLineEdit.textChanged.connect(self.model.title.setValue)
        self.view.vMaxDoubleSpinBox.valueChanged.connect(self.model.v_max.setValue)
        self.view.vMinDoubleSpinBox.valueChanged.connect(self.model.v_min.setValue)
        self.view.xAxisNameLineEdit.textChanged.connect(self.model.x_axis_name.setValue)
        self.view.yAxisNameLineEdit.textChanged.connect(self.model.y_axis_name.setValue)


    def _set_view_initial_values(self):
        self.view.axesColorColorButton.setColor(self.model.axes_color.value)
        self.view.axesLabelsColorColorButton.setColor(self.model.axes_labels_color.value)
        self.view.backgroundColorColorButton.setColor(self.model.background_color.value)
        self.view.centerLinesColorColorButton.setColor(self.model.center_lines_color.value)
        self.view.colormapComboBox.addItems(self.model.colormaps)
        self.view.colormapComboBox.setCurrentIndex(self.model.colormaps.index(self.model.colormap.value))
        self.view.dpiSpinBox.setValue(self.model.dpi.value)
        self.view.frameColorColorButton.setColor(self.model.frame_color.value)
        self.view.inputFileLineEdit.setText(self.model.input_file.value)
        self.view.isBackgroundTransparentCheckBox.setChecked(self.model.is_background_transparent.value)
        self.view.isCenterLinesDisplayedCheckBox.setChecked(self.model.is_center_lines_displayed.value)
        self.view.isShowFrameCheckBox.setChecked(self.model.is_show_frame.value)
        self.view.plotWidget.setAxesColor(self.model.axes_color.value)
        self.view.plotWidget.setAxesLabelsColor(self.model.axes_labels_color.value)
        self.view.plotWidget.setBackgroundColor(self.model.background_color.value)
        self.view.plotWidget.setCenterLinesColor(self.model.center_lines_color.value)
        self.view.plotWidget.setColormap(self.model.colormap.value)
        self.view.plotWidget.setFrameColor(self.model.frame_color.value)
        self.view.plotWidget.setIsBackgroundTransparent(self.model.is_background_transparent.value)
        self.view.plotWidget.setIsCenterLinesDisplayed(self.model.is_center_lines_displayed.value)
        self.view.plotWidget.setIsShowFrame(self.model.is_show_frame.value)
        self.view.plotWidget.setTicksColor(self.model.ticks_color.value)
        self.view.plotWidget.setTitle(self.model.title.value)
        self.view.plotWidget.setTitleColor(self.model.title_color.value)
        self.view.plotWidget.setVMax(self.model.v_max.value)
        self.view.plotWidget.setVMin(self.model.v_min.value)
        self.view.plotWidget.setXAxisName(self.model.x_axis_name.value)
        self.view.plotWidget.setYAxisName(self.model.y_axis_name.value)
        self.view.ticksColorColorButton.setColor(self.model.ticks_color.value)
        self.view.titleColorColorButton.setColor(self.model.title_color.value)
        self.view.titleLineEdit.setText(self.model.title.value)
        self.view.vMaxDoubleSpinBox.setValue(self.model.v_max.value)
        self.view.vMinDoubleSpinBox.setValue(self.model.v_min.value)
        self.view.xAxisNameLineEdit.setText(self.model.x_axis_name.value)
        self.view.yAxisNameLineEdit.setText(self.model.y_axis_name.value)