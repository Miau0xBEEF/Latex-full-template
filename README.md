# Latex-full-template
A full latex template with all convinient settings 

### creating an image-function
#### creating the template 
```
% Define the custom command
\newcommand{\insertfigure}[4]{
  \begin{figure}[H]
    \centering
    \includegraphics[width=#2]{#1}
    \caption{#3}
    \label{#4}
  \end{figure}
}
```
#### example of use 

```
% Define the custom command
\insertfigure{pic/myPic.png}{1.0\textwidth}{Caption of myPic}{fig:label of myPic}
```



