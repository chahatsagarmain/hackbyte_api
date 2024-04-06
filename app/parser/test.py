import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
import boto3
import os
from botocore import client
from pydantic import BaseModel
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma

import google.generativeai as genai
os.environ["GOOGLE_API_KEY"]="AIzaSyA2xj6zQDRQ6Nd08SncwBkIDC40G6YDTVk"
genai.configure( api_key=os.getenv("GOOGLE_API_KEY"))
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=os.getenv("GOOGLE_API_KEY"))

list=['Chahat Sagar\n(cid:131) 8210206586 #chahatsagar2003@gmail.com (cid:239)linkedin.com/chahatsagar §github.com/chahatsagarmain\nEducation\nIndianInstituteofInformationTechnologyandManagement ExpectedMay2026\nBachelorofTechnologyinInformationTechnology(CGPA:8.33) Gwalior,MadhyaPradesh\nTechnical Skills\nLanguages:Python,TypeScript,C++,SQL,Bash\nBackend:ExpressJS,Django,FastAPI,React.JS,GraphQL,WebSockets,Prometheus,Grafana\nDevOps:Docker,AWS,Terraform,Kubernetes,Nginx,Jenkins,GithubActions\nDatabases:MySQL,PostgresSQL,MongoDB,Redis,AWSDynamoDB\nTools:Git,Linux,VSCode\nCoursework\nDataStructures,Algorithms,ObjectOrientedProgramming,ComputerNetworking,OperatingSystems,\nDatabaseManagementSystem\nProjects\nCodeRunner|React.js,Django,Nginx,AWS,Docker,GitHubActions,ExpressJS,SocketIO\n• OrchestratedtheintegrationofReact.js,Django,Nginx,Docker,AWS,andExpressJStodevelopascalable\nmicroservice-basedremotecodeexecutionplatform.', '• ImplementedDockerforcontainerizationandAWSEC2forseamlessdeploymentwithCI/CDpipeliningwith\nGitHubActions.\n• Engineeredandimplemented10+RESTfulAPIendpointsandWebSocketconnectiontoenablereal-timemultiuser\nfunctionalityforonlineplatform;facilitatedseamlesschattingexperience.\n• DevelopedfrontendwithReactJSwithseamlessuserexperienceanddeployedonVercelwithGitHubActions.\nCommuNet-MailingAutomation|Typescript,ExpressJS,Docker,Nginx,AWS,MongoDB,Jenkins,SonarQube\n• Architected4microservices-basedservicesforautomatingmailingprocessesfromthefrontendandLinkedInviaa\nChromeextension.\n• SpearheadedthecontainerizationofservicesusingDockerCompose,deployingonAWSEC2withSSLcertification\nonapublicdomain;orchestratedtheprocessthroughaJenkinsCI/CDpipeline,enhancingsystemsecurityand\nscalability.\n• DeployedahighlysecureuserauthenticationservicebyintegratingGoogleOAuth2andMongoDB,enabling\nseamlessCRUDoperationswithTypescriptandExpressJS.', '• Architectedanddeployedasuiteof10+RESTAPIendpointsonvariousservicesforCRUDoperations,OAuth2\nimplementation,andseamlessemailautomationwithGmailintegration\n• Developmentandimplemented2AWSLambdafunctionsoptimizingfrontenddatauploadstoS3,enablingseamless\nextractionofcriticalinformationfromuploadedexcel/csvfiles,streamliningdataprocessingby40%\nAchievements\n• Solvedover200+DSAquestionsonvariouscodingplatformslikeLeetCode,GeeksForGeeksetc.\n• EngagedinHackathonHackByte2.0hostedbyMLHinIIITDMJabalpur.']
Chroma.from_texts(list, embeddings).as_retriever()