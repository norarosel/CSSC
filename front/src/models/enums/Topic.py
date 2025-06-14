# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @author: Nora Rosel Zaballos - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
from enum import StrEnum

# Third-party src imports

# Imports from your apps


class Topic(StrEnum):
    adverseEvents = 'Adverse events'
    nutrition = 'Nutrition'
    mentalHealth = 'Mental health'
    qol = 'Quality of life'
    jobSecurityAccessToEmployment = 'Job security and access to employment'
    survivorshipCare = 'Survivorship care'
    AYACare = 'Adolescent and Young Adult care'
    lateEffects = 'Late effects'
    wellBeing = 'Well being'
    meditation = 'Meditation'
    comorbidity = 'Comorbidity'
    rehabilitation = 'Rehabilitation'
    physicalActivity = 'Physical activity'
    socialRehabilitation = 'Social rehabilitation'
    sexualLife = 'Sexual life'
    lifeStyle = 'Lifestyle'
    empowermentOfCancerSurvivorship = 'Empowerment of cancer survivorship'
    inequalitiesInSurvivorship = 'Inequalities in survivorship'
    prevention = 'Prevention'
    cancerInformation = 'Cancer information'
    personalExperiences = 'Personal experiences'
