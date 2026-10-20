""" 
Configurações centralizadas da aplicação.

Todas as variáveis de ambiente são lidas, validadas e tipadas aqui.


Obs.: 
1. Nenhum outro módulo deve acessar 'os.environ' diretamente.

"""

from functools import lru_cache
from typing import Literal

from pydantic import AnyUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Configuração da aplicação carregadas a partir de variáveis de ambiente.

    A ordem de prioridade de leitura é:
    1. Variáveis de ambiente do sistema operacional;
    2. Arquivo .env na raiz do projeto;
    3. Valores padrão definidos aqui

    """


    # env_file diz onde está o arquivo de ambiente.
    # case_sensitive = False permite DATABASE_URL ou database_url no .env.
    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding= "utf-8",
        case_sensitive= False,
        extra = "ignore", # Ignora variáveis no .env que não estão declaradas aqui
    )

    # =========
    # Aplicação
    # =========
    app_name : str = "Financial API"
    app_version : str = "0.1.0"
    app_env : Literal["development", "staging", "production"] = "development"
    debug : bool = False

    
    # =========
    # API
    # =========
    api_v1_prefix : str = "/api/v1"


    # =========
    # Banco de Dados
    # =========
    database_url : AnyUrl 
    #AnyUrl será responsável valida o valor do URL.


    @field_validator("database_url", mode= "before")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """
        Garante que a URL do banco usa o driver assíncrono correto.

        O SQLAlchemy requer 'postgresql+asyncpg://' para operações async.
        Este validator corrige automaticamente 'postgresql://' para evitar erros silenciosos de configuração.

        """
        
        if isinstance(v, str) and v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return str(v)


    # =========
    # Segurança - JWT
    # =========
    secret_key: SecretStr # tipo especial do Pydantic que mascara o valor
    algorithm: str = "HS256"
    acess_token_expire_minutes: int = 30

    # em repr() e str(). Tente print(settings.secret_key) — você verá
    # "**********" em vez do valor real. Crucial para evitar vazamentos em logs.


    # =========
    # CORS - Origens permitidas para requisipções cross-origin
    # =========
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]


    # =========
    # Rate Limiting
    # =========
    rate_limit_per_minute: int = 60


    # =========
    # Propriedades computadas (não lidas do .env)
    # =========
    @property
    def is_production(self) -> bool:
        """Retorna True apenas em ambientes de produção."""
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        """Retorna True em ambiente de desenvolvimento."""
        return self.app_env == "development"


    @property
    def database_url_str(self) -> str:
        """
        Retorna a DATABASE_URL como string pura.
        
        Necessário porque AnyUrl é um objeto Pydantic, não uma string, e o SQLAlchemy espera uma string ou objeto compatível.
        """
        return str(self.database_url)

    @property
    def secret_key_value(self) -> str:
        """
        Retorna o valor real da SECRET_KEY para uso interno em criptografia.

        Use esta propriedade apenas onde o valor é estritamente necessário (ex: geração de JWT). Nunca exponha em logs ou respostas de API.
        """
        return self.secret_key.get_secret_value()

    # =========
    # Instância global - padrão Singleton via cache
    # =========

@lru_cache
def get_settings() -> Settings:
    
    return Settings()

settings: Settings = get_settings()