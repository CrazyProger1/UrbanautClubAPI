from tbf.view import View


class MainView(View):
    class Meta:
        default = True
        path = 'main'

    async def handle_command(self, *args, **kwargs):
        print(args, kwargs)
