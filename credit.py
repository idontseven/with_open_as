from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from name import *
import json

with open('data.json','r') as file:
    notes = json.load(file)

app = QApplication([])
main_window = QWidget()
main_window.resize(2000,1300)
main_window.setWindowTitle('Smart Notes')
notes_window = QWidget()
notes_window.resize(200,200)

H = QHBoxLayout()
main_layout_V1_text_edit = QVBoxLayout()
main_layout_V2 = QVBoxLayout()
layout_h1 = QHBoxLayout()
layout_h2 = QHBoxLayout()
layout_h3 = QHBoxLayout()
layout_h4 = QHBoxLayout()

edit_note = QTextEdit()
list_notes = QListWidget()
label_list_notes = QLabel('Список заметок')
btn_add_note = QPushButton('Добавить заметку')
btn_del_note = QPushButton('Удалить заметку')
btn_save_note = QPushButton('Сохранить заметку')
list_tags = QListWidget()
label_list_tags = QLabel('Список тегов')
tags_enter = QLineEdit('')
tags_enter.setPlaceholderText('Введите тег...')
btn_addtag_to_note = QPushButton('Добавить к заметке')
btn_deltag_of_note = QPushButton('Открепить от заметки')
btn_search_ontag = QPushButton('Искать заметку по тегу')
main_layout_V1_text_edit.addWidget(edit_note)
main_layout_V2.addWidget(label_list_notes)
main_layout_V2.addWidget(list_notes)
layout_h1.addWidget(btn_add_note)
layout_h1.addWidget(btn_del_note)
layout_h2.addWidget(btn_save_note)
main_layout_V2.addLayout(layout_h1)
main_layout_V2.addLayout(layout_h2)
main_layout_V2.addWidget(label_list_tags)
main_layout_V2.addWidget(list_tags)
main_layout_V2.addWidget(tags_enter)
layout_h3.addWidget(btn_addtag_to_note)
layout_h3.addWidget(btn_deltag_of_note)
layout_h4.addWidget(btn_search_ontag)


main_layout_V2.addLayout(layout_h3)
main_layout_V2.addLayout(layout_h4)

H.addLayout(main_layout_V1_text_edit)
H.addLayout(main_layout_V2)
main_window.setLayout(H)

def show_text():
    key = list_notes.selectedItems()[0].text()
    try:
        edit_note.setText(notes[key]["текст"])
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
    except KeyError:
        s('Данная заметка повредилась,удалите ее чтобы она не нарушала скрипты в приложении',error)

def add_note():
    note_name,result = QInputDialog.getText(notes_window,'Название заметки','Дайте название заметке')
    if note_name and result != '':
        notes[note_name] = {"текст":" ","теги":[]}
        list_notes.addItem(note_name)
    else:
        if result:
            s('Вы не ввели название',error)
        else:
            pass            

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_tags.clear()
        list_notes.clear()
        edit_note.clear()
        list_notes.addItems(notes)
        with open('data.json','w') as file:
            json.dump(notes,file,)
    else:
        s('Заметка для удаления не выбрана',error)

def s(text,setwindowtitle):
    s = QMessageBox()
    s.setWindowTitle(setwindowtitle)
    s.setText(text)
    s.show()
    s.exec_()
    s.resize(400,200)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = edit_note.toPlainText()
        with open('data.json','w') as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
        s('Сохранение заметки прошло успешно',succesful)
    else:
        s('Заметка для сохранения не выбрана',error)

def add_tag_innote():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        if tags_enter.text() in probel or tags_enter.text() == '':
            s('Нельзя вводить пустое название',error)
            tags_enter.clear()
        else:
            tag = tags_enter.text()
            if not tag in notes[key]["теги"]:
                notes[key]["теги"].append(tag)
                list_tags.addItem(tag)
                tags_enter.clear()
            else:
                s('Такой тег уже есть',error)
            with open('data.json','w') as file:
                json.dump(notes,file)
    else:
        s('Заметка не выбрана чтобы на нее поставить тег',error)

def del_tag_ofnote():
    if list_notes.selectedItems():
        try:
            key = list_notes.selectedItems()[0].text()
            tag = list_tags.selectedItems()[0].text()
            notes[key]["теги"].remove(tag)
            list_tags.clear()
            list_tags.addItems(notes[key]["теги"])
            with open('data.json','w') as file:
                json.dump(notes,file)
        except IndexError:
            s('Тег не выбран',error)
    else:
        s('Заметка не выбрана',error)

def search_on_tag():
    tag = tags_enter.text()
    if btn_search_ontag.text() == "Искать заметку по тегу" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]: 
                notes_filtered[note]=notes[note]
        btn_search_ontag.setText("Сбросить поиск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif btn_search_ontag.text() == "Сбросить поиск":
        tags_enter.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        btn_search_ontag.setText("Искать заметку по тегу")
    else:
        pass


btn_search_ontag.clicked.connect(search_on_tag)
btn_deltag_of_note.clicked.connect(del_tag_ofnote)
btn_addtag_to_note.clicked.connect(add_tag_innote)
btn_save_note.clicked.connect(save_note)
list_notes.itemClicked.connect(show_text)
btn_del_note.clicked.connect(del_note)
btn_add_note.clicked.connect(add_note)
list_notes.addItems(notes)
main_window.show()
app.exec_()