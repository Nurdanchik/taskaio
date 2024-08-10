from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, CommandObject

from app.database.requests import set_user, set_task, del_task
import app.keyboards as kb

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer(
    'Welcome to todo bot!\n'
    'Enter /todos to see your todos\n'
    'Enter /add_todo "todoname" to add a todo\n'
    'Tap on a todo that you have done and want to complete.'
)
    
@user.message(Command('todos'))
async def todos(message: Message):
    await message.answer(text='Here are your todos:', reply_markup= await kb.tasks(message.from_user.id))
    
@user.callback_query(F.data.startswith('task_'))
async def delete_task(callback: CallbackQuery):
    await del_task(callback.data.split('_')[1])
    await callback.answer('Task done!')
    await callback.message.delete()
    await callback.answer('Tap to delete task or write down new one: ', reply_markup= await kb.tasks(callback.from_user.id))
    
@user.message(Command('add_todo'))
async def add_task(message: Message, command: CommandObject):
    if command.args:
        toadd = command.args.strip()  # Убираем лишние пробелы, если есть
        if len(toadd) > 100:
            await message.answer('The task is too long!', reply_markup=await kb.tasks(message.from_user.id))
            return  # Завершаем выполнение функции, чтобы не добавлять задачу

        await set_task(message.from_user.id, toadd)
        await message.answer('Task added!\nTap to delete task or use /add_todo "todoname":', reply_markup=await kb.tasks(message.from_user.id))
    else:
        await message.answer('Please provide a task after the command.')
