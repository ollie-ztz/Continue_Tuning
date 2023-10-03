## FAQ
* #### FAQ
    * ##### Common questions
    * ##### Responses for one reviewer
    * ##### Responses for one reviewer
    * ##### Responses for one reviewer
    * ##### Responses for one reviewer
## Common questions
* #### Contributions and applications of AbdomenAtlas-8K.
    Two contributions: A large-scale dataset of 8,448 annotated CT volumes and an active learning procedure that can quickly create many other large-scale datasets. Firstly, AbdomenAtlas-8K was a composite dataset that unified medical datasets from at least 26 different hospitals worldwide. In total, more than 60.6 x 10<sup>9</sup> voxels were annotated in AbdomenAtlas-8K in comparison with 4.3 x 10<sup>9</sup> voxels annotated in the existing public datasets. We scaled up the organ annotation by a factor of 15. Once released, AbdomenAtlas-8K can be used to benchmark existing segmentation models and foster medical foundation models for a range of downstream applications. Secondly, the proposed active learning procedure can generate an attention map to highlight the regions to be revised by radiologists, reducing the annotation time from 30.8 years to three weeks. This strategy can scale up annotations quickly for creating medical datasets or even natural imaging datasets.
* #### Source and permissions to release data.
    We have now elaborated on the source and permissions in Table 3 (supplementary). To clarify, we will only disseminate the annotations of the CT volumes separately, and users will retrieve the original CT volumes, if needed, from the original sources (websites). Everything we intend to create and license-out will be in separate files and no modifications are necessary to the original CT volumes. We have consulted with the lawyers at Johns Hopkins University, confirming the permissions of distributing the annotations based on the license of each dataset. We will further include detailed download instructions on our GitHub page.
## Responses for one reviewer
* #### Comprehensive description and comparison between AMOS, AbdomenCT-1K, TotalSegmentator and AbdomenAtlas-8K
    1. **A significantly larger number of annotated CT volumes.** TotalSegmentator, AMOS, and AB1K provided 1,204, 500, and 1,112 annotated CT volumes. AbdomenAtlas-8K provided 8,448 annotated CT volumes (around eight times larger).
    2. **A notably greater diversity of the provided CT volumes.** The CT volumes in AbdomenAtlas-8K were collected and assembled from at least 26 different hospitals worldwide, whereas the makeup of TotalSegmentator and AMOS was sourced from a single country. Specifically, TotalSegmentator was from Switzerland (biased to the Central European population) and AMOS was from China (biased to the East Asian population). While AbdomenCT-1K was from 12 different hospitals, our AbdomenAtlas-8K presents significantly more CT volumes (8,448 vs. 1,112) and more types of annotated classes (8 vs. 4). 
    3. **The manual annotation time was significantly reduced.** The creation of AbdomenAtlas-8K used an effective active learning procedure, reducing the annotation time from 30.8 years to three weeks (see the revised Section 3.3 for a detailed calculation). This is an important scientific attempt to put active learning into practical use.
    4. **Produce an attention map to highlight the regions to be revised.** The attention maps mentioned in our active learning procedure can accurately detect regions with a high risk of prediction errors (evidenced in Table 1). This capability enables annotators to quickly find areas that require human revision. As a result, it significantly reduces annotators' workload and annotation time by a factor of 533.

    The  following Table to signify the extension of this research over the previous ones.
    |  dataset name  | # of CT volumes  | # of annotated organs | # of hospitals | use of active learning |
    |  ----  | ----  |  ----  | ----  | ----  |
    | AMOS | 500 | 15 | 2 | No |
    | AbdomenCT-1K | 1,112 | 4 | 12 | No |
    | TotalSegmentator | 1,204 | 104 | 1 | No |
    | AbdomenAtlas-8K | 8,448 | 8 | 26 | Yes |

    —————————————————————————
