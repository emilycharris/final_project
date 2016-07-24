from app.models import QueueProgram

class CreateQueue(forms.Form):

    class Meta:
        model = QueueProgram
        fields = ['program', 'network']
