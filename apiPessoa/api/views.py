from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

class PessoaList(APIView):
    def post(self, request):
        try:
            serializer = PessoaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()              
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def get(self, request):
        try:
            lista_pessoas = Pessoa.objects.all()
            serializer = PessoaSerializer(lista_pessoas, many=True)
            return Response(serializer.data)
        except Exception:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PessoaDetalhes(APIView):
    def get(self, request, pk):
        try:
            if pk == "0":
                return JsonResponse({'mensagem': "O ID deve ser maior que zero."},
                                    status=status.HTTP_400_BAD_REQUEST)
            pessoa = Pessoa.objects.get(pk=pk)
            serializer = PessoaSerializer(pessoa)
            return Response(serializer.data)
        except Pessoa.DoesNotExist:
            return JsonResponse({'mensagem': "A Pessoa não existe"},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            if pk == 0:
                return JsonResponse({'mensagem': "O ID deve ser maior que zero."},
                                    status=status.HTTP_400_BAD_REQUEST)
            pessoa = Pessoa.objects.get(pk=pk)
            serializer = PessoaSerializer(pessoa, data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Pessoa.DoesNotExist:
            return JsonResponse({'mensagem': "A pessoa não existe"},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
            
    def delete(self, request, pk):
        try:
            pessoa = Pessoa.objects.get(pk=pk)
            pessoa.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Pessoa.DoesNotExist:
            return Response({'mensagem': 'A pessoa não existe'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'mensagem': 'Ocorreu um erro no servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CalcularPesoIdeal(APIView):
    def get(self, request, pk):
        try:
            pessoa = Pessoa.objects.get(pk=pk)
            altura = pessoa.altura
            sexo = pessoa.sexo

            if sexo == 'M':
                peso_ideal = (72.7 * altura) - 58
            elif sexo == 'F':
                peso_ideal = (62.1 * altura) - 44.7
            else:
                return Response({'mensagem': "Sexo não reconhecido."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'pesoIdeal': peso_ideal})
        except Pessoa.DoesNotExist:
            return Response({'mensagem': "A pessoa não foi encontrada."}, status=status.HTTP_404_NOT_FOUND)

def index(request):
    return render(request, 'index.html')