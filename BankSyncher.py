import requests
import time
from datetime import datetime
import pyodbc
import os


TOKEN= os.environ.get('INQOM_TOKEN', None)


class JDCBankSyncher: 

	def __init__(self):
		self.dossiersToSync = []

	def obtainDossiersToSync(self): 
		os.environ['http_proxy'] = os.environ.get('FIXIE_URL', '')
		server = os.environ.get('INQOM_SERVER', None)	
		database = 'FredProdDb'
		username = "fredreader"
		password = os.environ.get('INQOM_DB', None)	
		cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};Server='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

		cursor = cnxn.cursor()
		cursor.execute ("SELECT DISTINCT bt.EnterpriseId FROM Banking.[Transaction] bt \
						JOIN Banking.Account ba ON bt.AccountId = ba.Id \
						JOIN EnterpriseExercise ee ON bt.EnterpriseId = ee.EnterpriseId AND bt.OperationDate<=ee.EndDate AND bt.OperationDate>=ee.BeginDate \
						JOIN BookAccountAssociation baa ON (baa.SourceId = ba.Id AND bt.EnterpriseId = baa.EnterpriseId) \
						WHERE ba.Provider = 4 \
						AND ee.Locked = 0 \
						AND bt.IsSynchronized = 0")

		self.dossiersToSync = [ x[0] for x in cursor.fetchall()]
		os.environ.pop('http_proxy')

	def syncDossiers(self):
		url = 'https://wa-fred-banking-prod.azurewebsites.net/api/app/banking/synchronization/transactions/synchronized?enterpriseId={dossierId}'
		headers = {"Authorization" : "Bearer "+TOKEN, "content-type":"application/json", 'accept':'application/json, text/plain; */*'}

		for index,list_item in enumerate(self.dossiersToSync):
			print (str(datetime.now())+ " : en traitement => dossier "+ str(list_item) + " | " + str(index+1) + " de " + str(len(self.dossiersToSync)))
			try:
				r = requests.post(url.format(dossierId = list_item), headers=headers)
			except requests.exceptions.HTTPError as err:
				raise SystemExit(err)

			print("Statut : " + str(r.status_code))
			time.sleep(0.5)


if __name__ == "__main__":
	jdc = JDCBankSyncher()
	jdc.obtainDossiersToSync()
	jdc.syncDossiers()
