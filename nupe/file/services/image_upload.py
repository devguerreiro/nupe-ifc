from os import remove

from nupe.file.models import ProfileImage


class ProfileImageService:
    def remove_file(self, profile_image: ProfileImage):
        """
        Remove o arquivo da imagem de perfil do diretório

        Argumentos:
            profile_image (ProfileImage): instância de ProfileImage que contém o path
        """
        if profile_image:
            remove(profile_image.image.path)
