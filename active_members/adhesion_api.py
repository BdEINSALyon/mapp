from json import JSONDecodeError
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests_oauthlib import OAuth2Session
from rest_framework import status
from rest_framework.exceptions import APIException

from mapp import settings
import logging
logger = logging.getLogger('adhesion_api')


class AdhesionAPI():
    url = settings.ADHESION_URL
    client_id = settings.ADHESION_CLIENT_ID
    client_secret = settings.ADHESION_CLIENT_SECRET
    token = None
    client = None
    oauth = None
    def __init__(self):
        self.refresh_token()
        super().__init__()

    @classmethod
    def refresh_token(self, needsRefresh=False):
        try:
            if (self.token is None and self.client is None) or needsRefresh:
                if needsRefresh: logger.info("Renouvellement du token car il est invalide")
                self.client = BackendApplicationClient(client_id=self.client_id)
                self.oauth = OAuth2Session(client=self.client)
                self.token = self.oauth.fetch_token(token_url=self.url + '/o/token/', client_id=self.client_id,
                                                    client_secret=self.client_secret)
                logger.info("Got token {} for external API".format(self.token['access_token']))
            else:
                logger.debug("Il y a dejà un Token : {} pour {}".format(self.token, self.client))
            #    r =self.client.refresh_token(self.url + '/o/token/') #ne faut-il pas le récupérer ??
            #    logger.debug(r.text)
        except:
            logger.exception("Impossible d'obtenir un token pour l'API externe Adhésion")

    def get(self, url, **kwargs):
        logger.info('api_va: GET {}'.format(url))
        import requests
        r = requests.get(url, headers={'Authorization': "Bearer "+self.token['access_token']}, **kwargs)
        logger.info("Réponse Adhésion ({}) : {}".format(str(r.status_code), r.text))
        if r.status_code == 401:
            logger.warning("Token expiré, on réessaie")
            self.refresh_token(needsRefresh=True) #visiblement y'a pas de refresh token avec une Application "client credentials"
            r = requests.get(url, headers={'Authorization': "Bearer " + self.token['access_token']}, **kwargs)
        if r.status_code not in [status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_202_ACCEPTED, status.HTTP_404_NOT_FOUND]:
            raise APIException("Une erreur est survenue lors de la connexion à un serveur externe")
        return r
        #try:
        #    r = self.oauth.get(url, **kwargs, timeout=10)
        #    if r.status_code ==401:
        #        raise TokenExpiredError
        #    return r
        #except TokenExpiredError:
        #    self.client.refresh_token(url+'/o/token/')
        #    logger.info("Credentials expirés ? le token a été refresh")
        #        #self.__init__() sinon on peut aussi en redemander
        #except Exception:
        #    logger.exception("Impossible de se connecter à {} pour l'API externe".format(url))

    def get_member_email(self, email):
        url = self.url+'/v1/members/?search=' + format(email)
        print(url)
        r = self.get(url)
        print (r)
        try:
            if r.status_code == 404: return None
            member = r.json()
            return member["results"]
        except KeyError: #keyerror si membre inexistant
            logger.exception(r.text)
            print("key error")
            return None
        except AttributeError: #pas de réponse
            print("Attribute")
            logger.exception(" ?")
            return None

    def get_member_id(self, id):
        url = self.url+'/v1/members/' + format(id)
        print(url)
        r = self.get(url)
        print (r)
        try:
            if r.status_code == 404: return None
            member = r.json()
            return member
        except KeyError: #keyerror si membre inexistant
            logger.exception(r.text)
            print("key error")
            return None
        except AttributeError: #pas de réponse
            print("Attribute")
            logger.exception(" ?")
            return None