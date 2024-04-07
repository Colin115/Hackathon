# Hackathon

Hackathon Repository

## Inspiration

Throughout our many interactions on the internet, we constantly run into the question of if the person on the other side of this interaction is real. Weather you're talking to a new friend on Instagram or a new love interest on Tinder, there's always a chance that you are just getting led on and catfished by the other side. This worry has continued to grow even more recently as major companies like X (twitter) now allow you to pay for your verification. This allows many people to falsely verify their identity. To combat this issue, we created Identity Solutions to help verify users online social media accounts.

## What it does

Identity Solutions offers a streamlined method for individuals to verify their identity and integrate their social media profiles with it. Users simply upload a photo of their state ID along with a selfie, leveraging advanced photo recognition technology to authenticate their identity. Upon verification, users gain the ability to connect their social media accounts to their profile. Once linked, these accounts are marked as verified. That way when other users search for your username on Identity Solutions, your account will prominently display the verified status.

## How we built it

Building Identity Solutions involved the creation of a full-stack website. We utilized Flask for our backend development and HTML for our frontend interface. Additionally, we integrated DeepFace to assist with facial recognition ensuring robust identity verification. This combination of technologies allowed us to create the perfect way to verify your social media presence.

## Challenges we ran into

One challenge we faced was refining our facial recognition algorithms, especially when matching small photos from IDs, which presented a significant hurdle. Through extensive research and numerous attempts, we persevered and eventually found the solution, with invaluable assistance from Stack Overflow.

Another obstacle we encountered was managing our project within the given timeframe. Developing a full website proved to be a time-consuming task, as we discovered over the weekend. However, we mitigated this challenge by crafting a detailed plan. By laying out everything we needed in advance, we we always knew our next steps, enabling us to overcome time constraints and deliver a successful project.

## Accomplishments that we're proud of

Given that this was our team's debut at the hackathon, we're immensely proud to have made it through the weekend. Completing the project we set out to accomplish is a significant achievement for us. Initially, our aim was to produce something that would suffice as a decent submission. However, upon reviewing our final project, we've excitedly realized that it surpasses our expectations and is a great submission.

## What we learned

Throughout the hackathon we learned many valuable lessons. One of the more valuable lessons we learned was planning pays off. By creating a plan to go off of it allowed us to stay much more organized than if we hadn't. We also learned that communication is very valuable. In the beginning we tried to work through all our problems on our own, but later on we started talking them out with each other. After we started talking them out, we started making progress much faster.

## What's next for Identity Solutions

It is our plan to continue developing Identity Solutions. We hope to grow this software as it solves a major problem in our increasingly virtual society. By further enhancing its capabilities and functionalities, we aim to establish Identity Solutions as a trusted solution for identity verification in online interactions.

### Use

```bash
pip install -r requirements.txt
python app.py
```
