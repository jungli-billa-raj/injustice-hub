Here are all the planning related to this project called Injustice Hub. 
This is currently aimed to be a MVP. Many more features will be required in the future. But for now, the goal is to ship a good enough product as soon as possible. 

1. Understand the problem. 
-> In a country like India, bad news comprise major part of daily news. This has made people somewhat insensitive and indifferent to the pain and sufferings happening to the people of this nation on a daily basis. Now, I by no means expect a software to eradicate this collosal problem. But, wouldn't it be great to have a software that can provide you the details of all the crimials(both individuals and organizations) between a 'start_date' and 'end_date' ? 
Also, the bias of media shouldn't be a problem here as the facts don't change, only the presentation does in these criminal cases. 
This seems novelty at first but it will really be of great use. (a.) It will not let people forget. Even if the people forget, the database will remember. (b.) For a future justice seeking entity, this database will be a goldmine of identifying the perpetrators. 

2. Requirements: 
  1. Features:
    a) Provide a structured data of all injustices. The columns will be "Blamed Entity(Individual or Collective Entity)", "Location", "Crime(A subjective description)", "Severity(1 to 10)", "Blame Status(Accused/Guilty/Liable)", "Justice Status(served/pending/escaped)".
    b) Give an overview based on the column data in Visual form. Say, Pie Chart, Bar Graph, Geography based analysis, etc. 
    c) Look at previous results.

  2. Tech:
    a) Python  
      * Scrapy -> Scrape News Articles. 
      * FastAPI -> to serve the endpoints. 
    b) HTML/CSS/JS -> I'm not really sure how to create the frontend for this. I'll need some help in deciding the suitable minimal tech stack for this. Svelte, perhaps. I'm not sure. 
    c) LLM API-> An LLM agnostic module to make requests and get intelligent results. This will be helpful in classification, summarizing, etc. This part must be LLM agnostic as right now I'll deploy a LLM locally on a different machine in the same wifi. Later, I should be able to use OpenAI or Claude's API if I get funding. I want an abstraction layer for this. 
    d) Sqlite -> A simple sql database for storing data and displaying them on the frontend. This should save all results and past results could be queried to show on the frontend. 

3. Goals: 
-> The current goal is just to have a minimal working product in 5 days. I believe in improving the product with time. For that I want good modular design. Speed is not a concern for now. Neither is quality of results. 

I want your help with:
1. Thinking about the design of this huge web scraping project. 
2. Things I probably missed. 
3. Time based deadline schedule. I know that this is not a good thing for learning. But enough learning, I want to build this thing. It's depressing to see these filthy news everyday and feel helpless. I want to make a change. 




----------------------------------------------------

1. We have successfully created a spider to extract archived news articles for any year after 1997 🤪.
2. We have also laid the foundation for our LLM abstraction and pipeline which includes JSON Validation, DB insertion etc. 
3. We have also written a script to populate the cases table in our database injustice.db with articles that are not processed already. 

Here's what I'm thinking. This however is by no means a new direction for our project. Please stick with the plan you had proposed before we started coding this project. This is just what I've in back of my mind for what Injustice Hub should look and feel like. 
1. I would like to include one more LLM call for each article which will simple take the headline of the article and tell if it's a crime or not. I'll obviously run it before processing results to save in 'cases' table. 
2. I'm wondering about what if Indian Express bans me or my Private IP. Then I'm fkked. 
3. Just for the sake of delivering a MVP, I'm thinking of scraping and populating my DB with news articles of one year, say 2025. Then, I'll process the articles and place them in cases table. Finally, I can work on the frontend to show what Injustice Hub is all about. 
