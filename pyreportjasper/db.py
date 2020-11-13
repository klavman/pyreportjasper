# -*- coding: utf-8 -*-
# GNU GENERAL PUBLIC LICENSE
#
# Copyright (c) 2020 Jadson Bonfim Ribeiro <contato@jadsonbr.com.br>
#

import jpype
import jpype.imports

from pyreportjasper.config import Config


class Db:
    Connection = None
    DriverManager = None
    Class = None
    JRXmlDataSource = None
    JsonDataSource = None
    JsonQLDataSource = None

    def __init__(self):
        self.Connection = jpype.JPackage('java').sql.Connection
        self.DriverManager = jpype.JPackage('java').sql.DriverManager
        self.Class = jpype.JPackage('java').lang.Class
        self.JRXmlDataSource = jpype.JPackage('net').sf.jasperreports.engine.data.JRXmlDataSource
        self.JsonDataSource = jpype.JPackage('net').sf.jasperreports.engine.data.JsonDataSource
        self.JsonQLDataSource = jpype.JPackage('net').sf.jasperreports.engine.data.JsonQLDataSource

    def get_xml_datasource(self, config: Config):
        ds = self.JRXmlDataSource(config.get_data_file_input_stream(), config.xmlXpath)
        return jpype.JObject(ds, self.JRXmlDataSource)

    def get_json_datasource(self, config: Config):
        ds = self.JsonDataSource(config.get_data_file_input_stream(), config.jsonQuery)
        return jpype.JObject(ds, self.JsonDataSource)

    def get_jsonql_datasource(self, config: Config):
        ds = self.JsonQLDataSource(config.get_data_file_input_stream(), config.jsonQLQuery)
        return jpype.JObject(ds, self.JsonQLDataSource)

    def get_connection(self, config: Config):
        dbtype = config.dbType
        host = config.dbHost
        user = config.dbUser
        passwd = config.dbPasswd
        driver = None
        dbname = None
        port = None
        sid = None
        connect_string = None

        if dbtype == "mysql":
            driver = config.dbDriver
            port = config.dbPort or 3306
            dbname = config.dbName
            connect_string = "jdbc:mysql://{}:{}/{}?useSSL=false".format(host, port, dbname)
        elif dbtype == "postgres":
            driver = config.dbDriver
            port = config.dbPort or 5434
            dbname = config.dbName
            connect_string = "jdbc:postgresql://{}:{}/{}".format(host, port, dbname)
        elif dbtype == "oracle":
            driver = config.dbDriver
            port = config.dbPort or 1521
            sid = config.dbSid
            connect_string = "jdbc:oracle:thin:@{}:{}:{}".format(host, port, sid)
        elif dbtype == "generic":
            driver = config.dbDriver
            connect_string = config.dbUrl

        self.Class.forName(driver)
        conn = self.DriverManager.getConnection(connect_string, user, passwd)
        return conn