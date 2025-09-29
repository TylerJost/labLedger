# Lab Ledger
Lab ledger is a *micro* project meant to help you be a better computational biologist. Given a base directory, labLedger finds git repos and stores their commits for the past week. It then uses a summarization model to summarize your work.

## Motivation
Unlike wet-bench scientists, computationalists don't often have lab notebooks. Sometimes they have their own system, and this is mine.

> Commit early, commit often

This is an aphorism commonly used in software development, and I try and use it in my experimental work. To make better commits and to adequately log my progress, I try and write down my experiments and review them each week to tell if I understood what progress I made for the last week. This helps me better understand my code and better present my project.

## Installation

Install using pixi with `pixi install`. The only requirements are pytorch and the transformers library, but these are only necessary if you're looking for an automated summary.