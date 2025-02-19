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


## Bib-Resources 
Creating bib resources can be done by using the different types of bib entries. Convenient tools like JabRef can be very helpful in organizing your resources. 
> **Note:** Try to avoid the use of _ in a bib entry.
> **Note:** @electronic is not directly a type. 


# Shortcuts 

New Item              Enter -> [ctr+shift+i]
Compile Document      F1
textit                [shift + i]
bold                  [shift + b]
texttt                [ctrl + shift + t]
comment out region    [ctrl + t]
uncomment region      [ctrl + u]