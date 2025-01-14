from promptflow.core import tool
from promptflow.connections import AzureOpenAIConnection
from pydantic import BaseModel 
from openai import AzureOpenAI  
from typing import List  
import json

class Document(BaseModel):
    class Chunk(BaseModel):  
        id: str
        title: str
        paragraph: str
        keyphrases: List[str]
        summary: str

@tool
def python_tool(body: str, filename: str, openai: AzureOpenAIConnection) -> object:
    
    client = AzureOpenAI(  
        azure_endpoint=openai.api_base,  
        api_key=openai.api_key,  
        api_version="2024-08-01-preview"
    )

#Provide the answer and translate the search results into the same language as the user's question.
    prompt = '''
You are a legal document processor. Your task is to break a provided legal document into manageable chunks, either by paragraphs or clauses depending on the context. The output must be in JSON format. Each chunk should include an ID, title, text, key phrases, and a summary. Key phrases should emphasize dates, names, and the most important information in the context of the document. Use the following JSON structure as a template:  

```json
{
    "chunk": [
        {
            "id": "string",
            "title": "string",
            "paragraph": "string",
            "keyphrases": ["string"],
            "summary": "string"
        }
    ]
}
```

### Instructions:
1. **Chunking Rules:**
   - Break the text into chunks by paragraph if the paragraphs are short and self-contained.
   - Break by clause if the paragraphs are long or contain multiple legal provisions.

2. **For Each Chunk:**
   - **ID:** Assign a unique numeric ID starting from "1" and incrementing for each chunk.
   - **Title:** Extract or summarize the main subject of the paragraph or clause. If not explicitly stated, infer a short, descriptive title.
   - **Paragraph:** Include the full text of the paragraph or clause.
   - **Key Phrases:** Extract the most relevant terms or phrases. Focus on:
     - Dates
     - Names (people, organizations, places)
     - Critical terms or keywords related to the legal content
   - **Summary:** Write a concise summary of the paragraph or clause.

3. **Output:** 
   - Provide the output as valid JSON.
   - Ensure the structure is consistent with the provided template.

### Example Output:  
```json
{
    "chunk": [
        {
            "id": "1",
            "title": "Introduction to Contract Terms",
            "paragraph": "This contract is entered into on January 1, 2024, between Party A and Party B.",
            "keyphrases": ["January 1, 2024", "Party A", "Party B"],
            "summary": "This paragraph introduces the contract, specifying the date and parties involved."
        },
        {
            "id": "2",
            "title": "Obligations of Party A",
            "paragraph": "Party A agrees to provide services outlined in Schedule 1 within 30 days of signing this agreement.",
            "keyphrases": ["Party A", "Schedule 1", "30 days", "agreement"],
            "summary": "This paragraph outlines the obligations of Party A to deliver services as per Schedule 1 within a specified timeframe."
        }
    ]
}
```

  '''
    
    # openai_response = client.beta.chat.completions.parse(  
    #     model="gpt4o-mini",  
    #     messages=[  
    #         {"role": "system", "content": prompt},  
    #         {"role": "user", "content": body},  
    #     ],  
    #     response_format=Document,  
    # )  
    # try:  
    #     openai_sentiment_response_post_text = openai_response.choices[0].message.parsed  
    #     response = json.loads(openai_sentiment_response_post_text.model_dump_json(indent=2))
    #     print(response)
    # except Exception as e:  
    #     print(f"Error converting to JSON sentiment from OpenAI: {e}")
    #     return  

    outputdemo = {  
    "chunk": [  
        {  
            "id": "1",  
            "title": "Rejection of Seller's Terms",  
            "paragraph": "ANY TERMS AND CONDITIONS PROPOSED IN THE SELLER’S ACCEPTANCE OR IN ANY ACKNOWLEDGEMENT, INVOICE, OR OTHER FORM OF THE SELLER THAT ADD TO, VARY FROM, OR CONFLICT WITH THE TERMS HEREIN ARE HEREBY REJECTED. SUCH TERMS AND CONDITIONS SHALL NOT APPLY TO THE CONTRACT UNLESS ACKNOWLEDGED BY A WRITTEN INSTRUMENT EXECUTED BY AUTHORISED REPRESENTATIVES OF THE BUYER AND THE SELLER. DESPATCH OR DELIVERY OF THE GOODS BY THE SELLER TO THE BUYER SHALL BE DEEMED CONCLUSIVE EVIDENCE OF THE SELLER’S ACCEPTANCE OF THESE TERMS AND CONDITIONS.",  
            "keyphrases": ["Seller’s acceptance", "terms and conditions", "Buyer", "Seller", "despatch", "delivery"],  
            "summary": "This paragraph states that any conflicting terms proposed by the Seller are rejected unless formally accepted in writing, and that delivery of goods signifies acceptance of the terms."  
        },  
        {  
            "id": "2",  
            "title": "Definitions",  
            "paragraph": "(a) “Authority” means any competent authority to whose authority Buyer or its Customer’s operations are subject to. (b) “Buyer” shall mean the legal entity issuing the Purchase Order, which may be Contoso Ltd or its affiliates, which expression shall include its successors and permitted assigns. (c) “Contract” shall mean the agreement entered into between the Buyer and the Seller for the purchase of the Goods and/or Services. The terms and conditions of the Contract shall comprise the terms in the Buyer’s purchase order, the terms and conditions herein and all annexes, appendices, schedules, exhibits, supplemental agreements, specifications, plans, drawings, patterns, samples or other documents or conditions which may be incorporated by contract. (d) “Contract Price” shall mean the price payable to the Seller for the Goods and/or Services. (e) “Customer” shall mean any customer of the Buyer. (f) “days” shall mean a reference to calendar day unless expressly stated otherwise. (g) “Goods” shall mean the Goods described in the Contract which the Seller is required under the Contract to supply and shall include any operating/instruction manuals and maintenance manuals relating to the Goods. (h) “Purchase Order” means the purchase order for Goods and/or Services issued by the Buyer. (i) “Seller” shall mean the person, firm or corporation who by the Contract undertakes to supply the Goods or to render such other Services as may be required by the Contract which expression shall include its successors and permitted assigns. (j) “Services” shall mean the Services described in the Contract which the Seller is required under the Contract to perform. (k) “Serviceable” means a Good which fulfils the operational purpose for which it was initially designed for and which shall be certified in accordance with any relevant manufacturer instructions and specifications in accordance with the relevant maintenance manual and requirements of a relevant Authority, as the case may be.",  
            "keyphrases": ["Authority", "Buyer", "Contoso Ltd", "Contract", "Contract Price", "Customer", "Goods", "Purchase Order", "Seller", "Services"],  
            "summary": "This section provides definitions for key terms used throughout the contract, clarifying the roles and responsibilities of the Buyer and Seller, and outlining what constitutes Goods and Services."  
        },  
        {  
            "id": "3",  
            "title": "Establishment of the Contract",  
            "paragraph": "If the Seller fails to accept the Purchase Order for any reason whatsoever, the shipment by the Seller of any Goods or the furnishing or commencement of any Services ordered, or the acceptance of any payment by the Seller hereunder or any other conduct by the Seller that recognises the existence of a contract pertaining to the subject matter herein, may, at the Buyer’s election, be treated as an unqualified acceptance by the Seller of the Purchase Order and all terms and conditions herein.",  
            "keyphrases": ["Seller", "Purchase Order", "Goods", "Services", "Buyer"],  
            "summary": "This clause states that the Seller's actions, such as shipment of Goods or acceptance of payments, may be considered as acceptance of the Purchase Order and its terms, even if the Seller has not formally accepted it."  
        },  
        {  
            "id": "4",  
            "title": "Variations",  
            "paragraph": "Subject to Clause 13, no variation, amendment or addition will apply to the Contract unless expressly agreed upon in writing and signed by the parties’ respective authorised representatives.",  
            "keyphrases": ["Clause 13", "variation", "amendment", "Contract"],  
            "summary": "This clause stipulates that changes to the Contract can only be made through a written agreement signed by authorized representatives of both parties."  
        },  
        {  
            "id": "5",  
            "title": "Quality, Standard and Description",  
            "paragraph": "(a) Subject to Clauses 9 and 11, the Goods shall: (i) be new and conform in all respects with the specifications and other requirements or descriptions stated in the Contract; (ii) be of sound materials, design and workmanship; (iii) be equal in all respects to the samples, patterns or specifications provided or given by either party; (iv) be capable of any standard of performance specified in the Contract; (v) if the purpose for which they are required is indicated in the Contract either expressly or by implication be fit for that purpose; (vi) be of satisfactory quality; and (vii) be Serviceable. (b) The Services shall be: (i) performed using all due care and diligence, in accordance with the turnaround time specified; and (ii) performed in accordance with appropriate service bulletins, specifications provided by Customer, maintenance and overhaul manuals of the manufacturer of the Goods and the directives of the relevant Authority, as may be applicable. In addition, the Seller shall maintain a certificate of approval for the Services issued by the Authority at all times during the period of the Contract. The Services shall be deemed completed only if they meet all requirements and all applicable acceptance tests have been successfully completed under the Contract. (c) All documents, records, test reports, etc, relating to the production of the goods must be retained on file for evaluation for a contractually agreed upon period. Unless otherwise specified, this period shall be ten years. (d) If any Goods are to be provided and/or Services are to be performed by the Seller’s subcontractors (if such subcontracting is expressly allowed under the Contract or if the Buyer’s prior written approval has been obtained), the Seller shall be and remain fully responsible for the actions of its subcontractors. (e) If the Seller is required to provide Services on the premises of the Buyer or a Customer, the Seller shall, and shall procure its employees, directors, officers or agents who are working on the Buyer’s premises in connection with the Contract to, comply with all of the Buyer’s safety and security procedures, as may be amended from time to time, and shall take any and all necessary steps and precautions to prevent injury to any person or property during the duration of the provision of Services under the Contract. If required by the Buyer, Seller shall also provide all other certificates and permits necessary in order for Services to be provided on the premises of the Buyer or a Customer.",  
            "keyphrases": ["Clause 9", "Clause 11", "Goods", "Services", "quality", "satisfactory", "subcontractors"],  
            "summary": "This section details the quality standards that Goods and Services must meet, including specifications, performance standards, documentation retention, and responsibilities regarding subcontractors and safety on premises."  
        },  
        {  
            "id": "6",  
            "title": "Inspection and Testing",  
            "paragraph": "(a) Before dispatching the Goods, the Seller shall carefully inspect and test them for compliance with the Contract. The Seller shall, if requested by the Buyer, give the Buyer reasonable notice of such tests and the Buyer shall be entitled to be represented thereat. The Seller shall also, at the request of the Buyer, supply to the Buyer a copy of the Seller’s test sheets certified by the Seller to be a true copy. (b) Where inspection of any of the Goods, whether completed or in the course of production, is required by the Buyer, the Seller shall give the Buyer full and free access to the Seller’s works as and when required for that purpose and the Seller shall give the Buyer all facilities and applicable records, at any level of the supply chain involved in the order, as may be required therefore, at no cost to the Buyer. Where necessary, this free access shall also be extended to Customers and any applicable Regulatory Authorities or Agencies. (c) If, as a result of any inspection or test under Clause 5(a) or 5(b), the Buyer’s representative is of the reasonable opinion that the Goods do not comply with the Contract or are unlikely to comply upon completion of manufacture or processing, he may inform the Seller accordingly in writing and the Seller shall forthwith take such steps as may be necessary to ensure such compliance.",  
            "keyphrases": ["inspection", "testing", "Goods", "Contract", "Buyer", "subcontractors"],  
            "summary": "This section outlines the responsibilities of the Seller for inspecting and testing Goods before dispatch, providing access to the Buyer for inspections, and ensuring compliance with the Contract if any issues are identified."  
        }  
    ]  
}  

    return outputdemo