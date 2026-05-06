PS: Initial model (no BatchNorm, 1 conv layer, 4 hidden layers) had 0.90 accuracy.
Final round of testing: training accuracy = 0.9918 and testing accuracy = 0.9929. The numbers vary a bit in the description because there were multiple trials for testing different components, some of them were a part of the earlier trials where the neural net was not complete.


CONVOLUTION LAYER DESIGN:

INTRO:
I used a 32, 64, 64 pattern for filter sizes because through testing, I figure that 32 filter captures low-level edges really well, so that the 64 filters doesn't have to do as much computing by itself, which takes less time. But, the 64 filters is also necessary for capturing high level edges that can resemble complete shapes, and I figure that two 64 filters works well for accuracy. 


INITIAL INSPIRATION FOR 3 CONVOLUTION LAYERS:

A human eye can identify objects really well in the accumulaton of edges, starting from small edge (like the verticle leveling of the nose) to medium edges (like the circle of an pupil) and to larger objects (like faces). This was my original inpiration for having 3 convolution layers. I experimented with adding convolution layers, and two 64 seems to work the best without adding too much computation time and increasing accuracy by a  percent. An interesting thing to note is that having only 64 filters actually takes more computation time than having 32 filters and 64 filters. Might be because the 32 filters captures low-level edges better, reducing compute for 64 filters.

FOR DETAILED TRIAL AND ERROR:

2 layers of 32 filters and 1 layer of 64 filters: training accuracy around 0.98, testing accuracy around 0.99, computation cost around 27-43 seconds
1 layer of 32 filters and 2 layers of 64 filters: training accuracy around 0.99 and testing accuracy around 0.99 and a lot less computational cost: 13-25 seconds. 
2 layers of 32 and 64 filters: almost same accuracy as above, computational cost around 20 seconds

Thus, I chose 1 layers of 32 filters and 2 layer of 64 filters because it uses way less time.


KERNEL SIZES:

I tested between 5x5, 3x3 and 2x2 kernel sizes. Size 2x2 had a way more expensive computational cost and lowered the accuracy. Kernel 5x5 was probably too big because the accuracy also decreased a lot, so the balance was 3x3 in the end.


MAX POOLING:

I also discovered that the max pooling size is best at pool size 2x2 for this particular dataset. Any bigger will cause the model to lose accuracy (ex. 3x3 is too big). For this data set, having an even number works better since kernels won't go off the image. Having max pooling after each convolution layer was the best for scaling each layer to sharpen the most popping feature.


BATCH NORMALIZATION!!!!!

BatchNormalization was a game changer when my training accuracy peaked at 0.95 and my testing accuracy peaked at 0.97. It increased my training accuracy to 0.9859, and my testing accuracy to 0.9940. HOORAY TO BATCH NORMALIZATION! I needed to add normalization after each pooling layer and after the dense layer to stabilize the testing accuracy to 0.99 (It also helped decrease the training time!). I tried switching the location of batchNormalization and maxpooling, and the ordering of batchNormalization before maxpooling slightly helped the training accuracy than the other way around. This might be because normalization applied after pooling can suppress the most activated/highest-valued features from max pooling. Normalizing before pooling would make more sense, because it ensures stability and proper scaling from inputs to pooling, letting the pooling focus on the significant features.

A reason for not putting batchnormalization after the first 64 filters of convolution layers is because the accuracy for training actually decreased to 98 and training time is relatively the same, so an extra 2 layers might not be necessary.


DROPOUT FOR CONVOLUTION LAYER:

I initially had dropouts 0.2 after each pooling layer. But I am aware that the network has not really learned anything early on. So, when I removed the first 0.2 and only had a dropout of 0.2 after the second pooling, and a 0.5 after the dense layer, my training accuracy shot up to 0.9918, which has never happened before, but the testing accuracy slightly decreased to 0.9904 (overfitting). Thus, I decided to drop 0.3 after the second pooling, which effectively prevented this.


HIDDEN LAYER DESIGN:

I initially added 4 hidden layers but had only 1 convolution layer and no normalization, which only got 90 percent accuracy. I figure 0.5 dropout PER hidden layer was too much (and the accuracy land slided). But I had sucesss by changing the 2nd and 4rd to 256, which increased the accuracy to around 0.92. Eventually, as convolution layers increased, one hidden layer of 256 units was enough.


DROPOUT FOR HIDDEN LAYER:

At first I used 0.5 dropout after the dense layer, but come to think about it building 256 units and then not use half of them is quite unresourceful. So, I tried decreasing the dropout to 0.3, and the result is 0.9932 accuracy for training and 0.9937 accuracy for testing, which were relatively close!


BATCHNORMALIZATION AFTER DENSE LAYER:

This actually improved accuracy from 0.98 to 0.99 for training and testing.


TRADE OFFS BETWEEN ACCURACY, SPEED, AND COMPLEXITY:

Accuracy helps lower death-rates in reality (safety is really important), but overfitting can actually hinder the accuracy model and speed, the two crucial factors for identifying a road sign. So, I tried to simplify my model as much as possible for optimization and used dropouts to prevent overfitting while trying to aim for 0.99 testing accuracy.


THANK YOU FOR READING!!