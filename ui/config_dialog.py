from qt.core import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QIntValidator, QIcon, \
    QSlider, Qt, QHBoxLayout

class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.max_resolution = 480
        self.quality = 75
        self.encoding_type = 'JPEG'
        self.algorithm = 'BILINEAR'
        self.blur_radius = 1

        self.__encodingType = None
        self.__encodingInfoLabel = None
        self.__algorithmType = None
        self.__blur_radius = None

        self.setWindowTitle("Bulk Image Resizer")

        layout = QVBoxLayout()
        self._info_section(layout)
        self._resolution_section(layout)
        self._quality_section(layout)
        self._conversion_section(layout)
        self._algorithm_section(layout)
        self._blur_section(layout)
        self._btn_section(layout)
        self.setLayout(layout)

    def _info_section(self, layout):
        info_label = QLabel("<b>Attention!</b>")
        info_label2 = QLabel("There are height compression options! Try the default ones before proceeding.")
        info_label.setTextFormat(Qt.RichText)
        info_label.setAlignment(Qt.AlignCenter)
        info_label2.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        layout.addWidget(info_label2)
        layout.addSpacing(10)
        layout.addStretch(1)

    def _resolution_section(self, layout):
        label1 = QLabel('Please indicate the maximum resolution for images (applied to the shorter side):')
        self.input1 = QLineEdit()
        self.input1.setValidator(QIntValidator(100, 4000))
        self.input1.setText(str(self.max_resolution))
        layout.addWidget(label1)
        layout.addWidget(self.input1)

    def _quality_section(self, layout):
        label2 = QLabel('Please indicate the quality for webp codec conversion (it is ok to keep it at 100%):')
        self.input2 = QLineEdit()
        self.input2.setValidator(QIntValidator(5, 100))
        self.input2.setText(str(self.quality))
        layout.addWidget(label2)
        layout.addWidget(self.input2)

    def _conversion_section(self, layout):
        h_box_label = QHBoxLayout()
        tooltip_label = QLabel()
        icon = QIcon.ic('dialog_information.png')
        tooltip_label.setPixmap(icon.pixmap(16, 16))
        tooltip_label.setToolTip('PNG: compression is applied by reducing bitrate of colors\n'
                                 'JPEG: compression is based on human visual perception\n'
                                 'WebP: compression is based on predictive & entropy coding')
        h_box_label.addWidget(QLabel("Pick encoding type:"))
        h_box_label.addWidget(tooltip_label)
        h_box_label.setAlignment(Qt.AlignLeft)

        self.__encodingType = QComboBox(self)
        self.__encodingType.addItem('Keep current')
        self.__encodingType.addItem('PNG')
        self.__encodingType.addItem('JPEG')
        self.__encodingType.addItem('WebP')
        self.__encodingType.currentIndexChanged.connect(self.type_changed)
        self.__encodingInfoLabel = QLabel(self)
        self.__encodingInfoLabel.setStyleSheet('border: 2px solid red; padding: 8px;')
        self.__encodingInfoLabel.setText('<b>ATTENTION!</b> Currently there is <b>NO</b> handheld device that '
                                       'correctly support WebP format!')
        self.__encodingInfoLabel.setAlignment(Qt.AlignCenter)
        self.__encodingInfoLabel.setTextFormat(Qt.RichText)
        self.__encodingInfoLabel.hide()

        layout.addLayout(h_box_label)
        layout.addWidget(self.__encodingType)
        layout.addWidget(self.__encodingInfoLabel)

    def _algorithm_section(self, layout):
        h_box_label = QHBoxLayout()
        tooltip_label = QLabel()
        icon = QIcon.ic('dialog_information.png')
        tooltip_label.setPixmap(icon.pixmap(16, 16))
        tooltip_label.setToolTip('NEAREST: speed 6 [fastest] / quality Low\n'
                                 'BOX: speed 5 / quality Medium\n'
                                 'BILINEAR: speed 4 / quality Medium\n'
                                 'HAMMING: speed 3 / quality Medium\n'
                                 'BICUBIC: speed 2 / quality High\n'
                                 'LANCZOS: speed 1 [slowest] / quality Very High\n')
        h_box_label.addWidget(QLabel("Pick resizing algorithm:"))
        h_box_label.addWidget(tooltip_label)
        h_box_label.setAlignment(Qt.AlignLeft)

        self.__algorithmType = QComboBox(self)
        self.__algorithmType.addItem('NEAREST')
        self.__algorithmType.addItem('BOX')
        self.__algorithmType.addItem('BILINEAR')
        self.__algorithmType.addItem('HAMMING')
        self.__algorithmType.addItem('BICUBIC')
        self.__algorithmType.addItem('LANCZOS')

        layout.addLayout(h_box_label)
        layout.addWidget(self.__algorithmType)

    def _blur_section(self, layout):
        h_box_label = QHBoxLayout()
        tooltip_label = QLabel()
        icon = QIcon.ic('dialog_information.png')
        tooltip_label.setPixmap(icon.pixmap(16, 16))
        tooltip_label.setToolTip('Gaussian Blur aplitude: 0 (fastest / no blur) - 20 (slowest)')
        h_box_label.addWidget(QLabel("Select blur size (in pixels):"))
        h_box_label.addWidget(tooltip_label)
        h_box_label.setAlignment(Qt.AlignLeft)

        self.__blur_radius = QSlider(Qt.Horizontal)
        self.__blur_radius.setMinimum(1)
        self.__blur_radius.setMaximum(20)
        self.__blur_radius.setTickInterval(1)
        self.__blur_radius.setTickPosition(QSlider.TicksBelow)
        self.__blur_radius.setValue(0)

        layout.addLayout(h_box_label)
        layout.addWidget(self.__blur_radius)

    def _btn_section(self, layout):
        button_layout = QHBoxLayout()
        submit_button = QPushButton('OK')
        submit_button.clicked.connect(self.submit)
        button_layout.addWidget(submit_button)

        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def type_changed(self):
        selected_option = self.__encodingType.currentText()
        if selected_option == 'WebP':
            self.__encodingInfoLabel.show()
        else:
            self.__encodingInfoLabel.hide()

    def submit(self):
        self.max_resolution = int(self.input1.text())
        self.quality = int(self.input2.text())
        self.encoding_type = self.__encodingType.currentText()
        self.algorithm = self.__algorithmType.currentText()
        self.blur_radius = self.__blur_radius.value()
        self.accept()
