from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class MarketResrchCrew():
	"""MarketResrchCrew crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	from crewai import LLM
	import os

	# Explicitly define the Gemini LLM
	gemini_llm = LLM(
		model="gemini/gemini-3.1-flash-lite",
		api_key=os.environ.get("GEMINI_API_KEY")
	)

	@agent
	def market_research_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['market_research_specialist'],
			verbose=True,
			llm=self.gemini_llm
		)

	@agent
	def competitive_intelligence_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['competitive_intelligence_analyst'],
			verbose=True,
			llm=self.gemini_llm
		)

	@agent
	def customer_insights_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['customer_insights_researcher'],
			verbose=True,
			llm=self.gemini_llm
		)

	@agent
	def product_strategy_advisor(self) -> Agent:
		return Agent(
			config=self.agents_config['product_strategy_advisor'],
			verbose=True,
			llm=self.gemini_llm
		)

	@agent
	def business_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['business_analyst'],
			verbose=True,
			llm=self.gemini_llm
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def market_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['market_research_task'],
		)

	@task
	def competitive_intelligence_task(self) -> Task:
		return Task(
			config=self.tasks_config['competitive_intelligence_task'],
		)

	@task
	def customer_insights_task(self) -> Task:
		return Task(
			config=self.tasks_config['customer_insights_task'],
		)

	@task
	def product_strategy_task(self) -> Task:
		return Task(
			config=self.tasks_config['product_strategy_task'],
		)

	@task
	def business_analyst_task(self) -> Task:
		return Task(
			config=self.tasks_config['business_analyst_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the MarketResrchCrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
