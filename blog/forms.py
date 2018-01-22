from django import forms

from blog.models import Question, Comment


class QuestionForm(forms.ModelForm):
    phone_number = forms.RegexField(
        regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',
        max_length=13,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="연락처",
        error_messages={'invalid': "전화번호는 '010-1234-5678'혹은 '01012345678'형태로 입력하여야 합니다."}
    )

    class Meta:
        model = Question

        fields = (
            'name',
            'email',
            'phone_number',
            'password',
            'title',
            'content',
            'is_secret',
        )
        labels = {
            'name': '성함',
            'email': '이메일',
            'password': '글 암호',
            'title': '제목',
            'content': '내용',
            'is_secret': '비밀글',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
            'is_secret': forms.CheckboxInput(
                attrs={
                    'class': 'form-control text-left',
                }
            )
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'content',
        )
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
