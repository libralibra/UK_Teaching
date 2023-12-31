![Games Academy](../../Falmouth/common/ga_uni_logo.png)

![Assessment banner](./img/assessment_banner.png)
Source: image generated by <a href="https://huggingface.co/Joeythemonster/anything-midjourney-v-4-1" target="_blank">Joeythemonster/anything-midjourney-v-4-1</a>
Prompt: "_A sci-fi scene with dark background shown robots connect to neural networks_"

# Applications of Machine Learning Techniques

**COMP714: Machine Learning**
**Brief of Assignment 1**

Dr Daniel Zhang

Games Academy, Falmouth University
v 0.1 (2023-2024)

---

<div id="top" style="visibility: hidden;"></div>

# Table of Contents
- [Applications of Machine Learning Techniques](#applications-of-machine-learning-techniques)
- [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
    - [Problem Definition and Data Preparation](#problem-definition-and-data-preparation)
    - [Feature Selection](#feature-selection)
    - [Fundamental Machine Learning Experiments](#fundamental-machine-learning-experiments)
  - [Assignment Format](#assignment-format)
    - [Project Outline](#project-outline)
    - [Monitoring Your Progress](#monitoring-your-progress)
    - [Submit a Demonstration Video](#submit-a-demonstration-video)
    - [Attend the Viva](#attend-the-viva)
  - [Additional Guidance](#additional-guidance)
  - [FAQ](#faq)
  - [Marking Rubrics](#marking-rubrics)



## Introduction
[Top](#top)

This assignment entails a research project to showcase your comprehension of Machine Learning (ML) techniques. It provides an opportunity to experiment with ML frameworks explored during lectures and workshops. The objective is to create a small-scale machine-learning solution applicable to a specific task, such as controlling a game agent, content generation, analysing game-related datasets for prediction, or other suitable pursuits.

The project aims to address two fundamental ML questions for game-related AI:

- Can ML effectively accomplish a game-related task?
- How do varying parameters impact ML algorithm performance?

The assignment comprises the following sections:

### Problem Definition and Data Preparation
[Top](#top)

Commence your project by selecting a suitable problem and sourcing data for algorithmic work. This could involve a simple 2D game, an existing game framework, a dataset from the ML literature, or unconventional applications of well-known datasets like `mnist`. The choice must demonstrate originality or a new perspective. Familiarity with Python or `ML.Net` is recommended, with tools such as `PyGame`, `Turtle` for Python, and `MonoGame` for C# development.

Utilise learned techniques from `COMP712 - Classical Artificial Intelligence` for symbolic AI to generate training data. Design an easily adaptable AI for data output, essential for online learning.

### Feature Selection
[Top](#top)

Many datasets or games offer varied fields for ML algorithm training, necessitating adjustments or the creation of new features for optimal performance. Iterating on feature selection is integral to the ML process. Explore different features for AI input, selecting and modifying them based on feedback and experimentation stages.

> NOTE:
> Maintain records of attempted strategies and outcomes for the second assignment.

### Fundamental Machine Learning Experiments
[Top](#top)

Experiment with your chosen approach's parameters to assess algorithmic performance. Given the limited timeline (6 weeks), swift iterations and start of evaluation by week 3 are crucial. Avoid last-minute attempts at AI training, as it won’t yield results.

## Assignment Format
[Top](#top)

The assignment includes these parts:

### Project Outline
[Top](#top)

This single **formative** assessment involves presenting your research plan during the week 2 workshop. Briefly outline your chosen application as a testbed, targeted AI for ML, and an overview of data and ML processing.

### Monitoring Your Progress
[Top](#top)

A series of continuous **formative** assessments during weekly workshop sessions allow discussions on research progress, providing informal feedback.

### Submit a Demonstration Video
[Top](#top)

This **summative** submission involves preparing a 2-5 minute video demonstrating your ML application. Submit the video link via [Microsoft Streams](https://www.microsoft365.com/launch/stream) alongside your project repository link. Advanced editing is unnecessary; a raw screen capture is sufficient.

Formal feedback will be provided within 3 weeks.

### Attend the Viva
[Top](#top)

Participate in the scheduled viva session to discuss your work, constituting a **summative** submission. Informal feedback will be given during the viva.

## Additional Guidance
[Top](#top)

This research project requires careful planning and management. Approach it as an experiment, meticulously documenting each step and iteration in the ML process. Planning and time management are critical; commence work early and maintain a consistent pace, avoiding last-minute rushes.

Developing AI using symbolic and non-symbolic approaches demands significant effort and cannot be crammed before deadlines. There's a crucial phase of testing involved. Initiate work early, sustaining steady progress throughout the assignment.


## FAQ
[Top](#top)

1. **Q: What is the deadline of this assignment?**
   **A**: _<a href="https://myfalmouth.falmouth.ac.uk/" target="_blank">MyFalmouth</a>_ system is the only place where you should be able to find all deadline information according to the requirements and the policies of Falmouth University.

2. **Q: How can I seek help?**
   **A**: You can email the tutor for any informal clarifications. For short question, MS Teams message would work as well.

3. **Q: Will there be feedback on my work?**
   **A**: You will be given verbal feedback on your work during the assessment session. Please consider to book an appointment with the tutor if you need in-depth discussions.

4. **Q: Any other issues?**
   **A**: Any other issues or mistakes in this brief, please inform the tutor.


---

>**Note**: Please refer to the marking rubric for more detailed information regarding the criteria.

## Marking Rubrics
[Top](#top)


| Criterion                                  | Weight | Near Pass                                                                         | Pass                                                                                                                             | Merit                                                                                                                                                                                | Distinction                                                                                                                                                                                      |
| ------------------------------------------ | ------ | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Maintainability of data processing         | 20%    | Data processing appears adhoc and/or difficult to follow                          | Clear approach to data processing Some consideration to repeatability, although data processing steps may not be clear           | Clear data processing process Some consideration given to meta-training Some consideration given to robustness Some consideration given to repeatability                             | Clear data processing process Much consideration given to meta-training Robustness considerations form a core part of the solution Repeatability considerations form a core part of the solution |
| ML Pipeline                                | 10%    | There is no clear pipeline, or the program architecture is poorly considered.     | There is some attempt at a pipeline within the program, with a clear sequence of steps.                                          | There is a clear separation between learning/data processing and induction/‘production’ usage.                                                                                       | Pipeline is clear, and follows industry conventions. There is evidence of evaluation/iteration over the parameters or structure (and how this has been accomplished)                             |
| Robustness of ML integration               | 20%    | ML solution implemented but largely non-functional / non-working                  | Project implements ML functionality, but it is largely derived from off-the-shelf components                                     | Project implements ML functionality, with some consideration to parameter choice.                                                                                                    | Project implements ML functionality, with some novel or interesting insights                                                                                                                     |
| Maintainability of Solutions               | 10%    | The code submitted is hard to follow, and lacks either documentation or comments. | The solution is documented and is reasonably easy to follow Limited consideration for repeatability                              | Game AI is well-suited to ML approaches Comments are clear and understandable Good consideration for repeatability (eg, all required libraries and steps are documented in a readme) | Game AI that incredibly well suited to ML approaches Near industry standard level of commenting Very good consideration for repeatability                                                        |
| Scope of ML techniques                     | 20%    | Little consideration of ML techniques within submission                           | Some considerations for parameters and data processing Some evidence of investigation into different AI techniques or parameters | Reasonable consideration features, parameters, or hyper-parameters Good evidence of investigation into different AI techniques or parameters                                         | Good consideration of the chosen features, parameters, or hyper-parameters Excellent evidence of investigation into different AI techniques or parameters                                        |
| Suitability of chosen algorithms and topic | 20%    | Topic chosen is not suitable for the given project.                               | The topic chosen is reasonable if poorly scoped. The algorithm choice is reasonable for the task being considered                | The topic chosen is a good fit for the assignment and is well-scoped. The algorithm choice is suitable for the task being considered                                                 | The topic chosen is a good fit for the assignment and shows an innovative approach. Algorithm choice is informed by existing work and is well suited for the task                                |

*The above table was generated on <a href="https://www.tablesgenerator.com/markdown_tables" target="_blank">https://www.tablesgenerator.com/markdown_tables</a>

