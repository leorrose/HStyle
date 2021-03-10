import { TeamMember } from '../models/team-member';
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class TeamMemberService {

    constructor() { }

    /**
     * method to get application team members
     * @returns array of team members
     */
    getTeamMembers(): TeamMember[] {
        const teamMembers = [
            {
                name: 'Irina Rabaev',
                imagePath: 'assets/team_members_profiles/irena_profile.webp',
                description: `Dr. Irina Rabaev main research interests include the areas
                of computer vision and image processing with a focus on historical documents
                analysis. Irina is the academic advisor of this project.`,
                researchgateLink: 'https://www.researchgate.net/profile/Irina_Rabaev',
                linkedinLink: 'https://www.linkedin.com/in/irina-rabaev-3b621659/',
                githubLink: '',
                emailAddress: 'irinar@ac.sce.ac.il ',

            },
            {
                name: 'Leor Ariel Rose',
                imagePath: 'assets/team_members_profiles/leor_profile.webp',
                description: `Leor is a senior-year software engineering
                student with a passion for data science and machine learning.
                Leor is part of the research and development team.`,
                researchgateLink: '',
                linkedinLink: 'https://www.linkedin.com/in/leorrose/',
                githubLink: 'https://github.com/leorrose',
                emailAddress: 'Leor.rose@gmail.com'
            },
            {
                name: 'Yahav Bar David',
                imagePath: 'assets/team_members_profiles/yahav_profile.webp',
                description: `Yahav is a senior-year software engineering
                student in a data science specialization with a passion
                for the field. Yahav is part of the research and development team.`,
                researchgateLink: '',
                linkedinLink: 'https://www.linkedin.com/in/yahavbardavid/',
                githubLink: 'https://github.com/Yahavba',
                emailAddress: 'yahavba356@gmail.com'
            }
        ];

        return teamMembers;
    }
}
