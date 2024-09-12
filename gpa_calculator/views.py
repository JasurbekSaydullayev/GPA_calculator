from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from gpa_calculator.models import Subject, User
from gpa_calculator.serializer import UsersListSerializer, SubjectSerializer


class Register(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = []
    authentication_classes = []
    http_method_names = ['post']
    serializer_class = UsersListSerializer

    def create(self, request, *args, **kwargs):
        try:
            username = request.data['username']
            password1 = request.data['password1']
            password2 = request.data['password2']
            user = User.objects.filter(username=username).first()
            if user:
                res = {
                    'status': 0,
                    'msg': "Bunday foydalanuvchi mavjud"
                }
                return Response(res, status=status.HTTP_200_OK)
            if password1 != password2:
                res = {
                    'status': 0,
                    'msg': "Parollar mos emas"
                }
                return Response(res, status=status.HTTP_200_OK)

            user = User.objects.create(username=username)
            user.set_password(password1)
            user.save()
            res = {
                'status': 1,
                'msg': "Muvofaqqiyatli ro'yhatdan o'tildi"
            }
            return Response(res, status=status.HTTP_200_OK)
        except KeyError:
            res = {
                'status': 0,
                'msg': "Please set all required fields. Required fields: username, key"
            }
            return Response(res, status=status.HTTP_200_OK)


class GPAViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    permission_classes = []
    authentication_classes = []
    http_method_names = ['get', 'post']
    serializer_class = SubjectSerializer

    def list(self, request, *args, **kwargs):
        try:
            username = request.query_params.get('username')
            user = User.objects.filter(username=username).first()
            if not user:
                user = request.user
                if not user.is_authenticated:
                    res = {
                        'status': 0,
                        'msg': "User not found"
                    }
                    return Response(res, status=status.HTTP_200_OK)
            info = []
            gpa_grade = 0
            subject_credits = 0
            subject_score = 0
            subjects = user.subjects.all()
            if subjects:
                for subject in subjects:
                    score = subject.score
                    credit = subject.credit
                    if score >= 90 and score <= 100:
                        grade = 5
                    elif score < 90 and score >= 70:
                        grade = 4
                    elif score < 70 and score >= 60:
                        grade = 3
                    else:
                        grade = 0
                    subject_credits += credit
                    subject_score += score * credit
                    gpa_grade += grade * credit
                    info.append({'Fan nomi': f"{subject.name}",
                                 'Ball': f"{score}",
                                 'Baho': f"{grade}",
                                 'Kredit miqdori': f"{credit}", })
                res = {
                    'status': 1,
                    "O'rtacha ball fozida": f"{subject_score / subject_credits}",
                    "GPA": f"{gpa_grade / subject_credits}",
                    "username": f"{user.username}",
                    'data': info
                }
                return Response(res, status=status.HTTP_200_OK)
            else:
                res = {
                    'status': 0,
                    'msg': "Ushbu foydalanuvchida GPA ma'lumotlari yo'q"
                }
                return Response(res, status=status.HTTP_200_OK)
        except KeyError:
            res = {
                'status': 0,
                'msg': "Please set all required fields. Required fields: username"
            }
            return Response(res, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            username = data['username']
            key = data['key']
            subject_name = data['subject_name']
            subject_score = data['subject_score']
            subject_credit = data['subject_credit']
            user = User.objects.filter(username=username, key=key).first()
            if not user:
                res = {
                    'status': 0,
                    'msg': "Foydalanuvchi topilmadi"
                }
                return Response(res, status=status.HTTP_200_OK)
            subject = Subject.objects.filter(name=subject_name, user=user).first()
            if not subject:
                Subject.objects.create(user=user, name=subject_name, score=subject_score, credit=subject_credit)
                res = {
                    'status': 1,
                    'msg': "Saqlandi",
                    'subject_name': subject_name,
                    'subject_score': subject_score,
                    'subject_credit': subject_credit
                }
                return Response(res, status=status.HTTP_200_OK)
            else:
                old_data = {
                    'subject_name': subject.name,
                    'subject_score': subject.score,
                    'subject_credit': subject.credit
                }
                subject.delete()
                Subject.objects.create(user=user, name=subject_name, score=subject_score, credit=subject_credit)
                res = {
                    'status': 1,
                    'msg': "Saqlandi",
                    'old_data': old_data,
                    'new_data': {
                        'subject_name': subject_name,
                        'subject_score': subject_score,
                        'subject_credit': subject_credit
                    }
                }
                return Response(res, status=status.HTTP_200_OK)
        except KeyError:
            res = {
                'status': 0,
                'msg': "Please set all required fields. Required fields: username, key, subject_name, subject_score, subject_credit"
            }
            return Response(res, status=status.HTTP_200_OK)
