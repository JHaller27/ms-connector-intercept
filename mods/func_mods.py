from typing import Callable, Any

class FuncMods:
	def __init__(self) -> None:
		self._mods: list[Callable[[Any], Any]] = []
		self._active = True

	def add(self, func):
		if self._active:
			self._mods.append(func)
		return func

	def run(self, obj: Any) -> Any:
		for m in self._mods:
			obj = m(obj)
		return obj

	def passthrough(self, obj: Any) -> Any:
		return obj

	def deactivate(self):
		self._active = False

	def activate(self):
		self._active = True
