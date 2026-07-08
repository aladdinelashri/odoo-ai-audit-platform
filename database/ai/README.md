# AI Engine

## Components

- QueryParser
- IntentDetector
- EntityDetector
- ParameterDetector

- ExecutionPlanner

- SkillEngine
    - NumericSkill
    - DateSkill
    - StateSkill
    - AggregateSkill

- SQL Engine

## Flow

User

↓

Query Parser

↓

Execution Planner

↓

Skill Engine

↓

Execution Plan

↓

SQL Builder

↓

SQL

↓

Database
