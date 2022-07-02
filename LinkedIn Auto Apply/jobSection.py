class Search:
    def multiple_bool_filter(self, string, keys, bools):
        Tcount = bools.count(True)
        added = 0
        if Tcount==0:
            return

        for k in range(len(bools)):
            if bools[k]:
                string += keys[k]
                if Tcount!=added:
                    string += '%2C'
                else:
                    break
        return string

    def where(self, string):
        string = string.replace(',', '%2C')
        string = string.replace(' ', '%20')

        return 'location=' + string

    def keywords(self, keyword):    
        return f'keywords={keyword}'

    def remote_filter(self, onsite, remote, hybrid):
        string = 'f_WT='
        keys = ['1', '2', '3']
        bools = [onsite, remote, hybrid]

        string = self.multiple_bool_filter(string, keys, bools)
        return string

    def date_posted_filter(self, anytime, past_month, past_week, past24hrs):
        if not anytime and not past_month and not past_week and not past24hrs:
            return
        if anytime:
            return
        if past_month:
            num = '2592000'
        if past_week:
            num = '604800'
        if past24hrs:
            num = '86400'
        return f'f_TPR=r{num}' 

    def experience_filter(self, internship, entry_lvl, associate):
        string = 'f_E='
        keys = ['1', '2', '3']
        bools = [internship, entry_lvl, associate]

        string = self.multiple_bool_filter(string, keys, bools)
        return string

    def job_type_filter(self, full_time, part_time, contract, temporary, volunteer, internship, other):
        string = 'f_JT='
        keys = ['F', 'P', 'C', 'T', 'V', 'I', 'O']
        bools = [full_time, part_time, contract, temporary, volunteer, internship, other]

        string = self.multiple_bool_filter(string, keys, bools)
        return string

    def easy_apply_filter(self, Bool):
        if Bool:
            return 'f_AL=true'
        else:
            return

    def under_10_applicants_filter(self, Bool):
        if Bool:
            return 'f_EA=true'
        else:
            return

    def sort_by_search(self, relevant, date_posted):
        if relevant:
            return 'sortBy=R'
        else:
            return 'sortBy=DD'

    def filters(self, 
        location,
        keyword,    
        onsite, remote, hybrid,
        anytime, past_month, past_week, past24hrs,
        internship, entry_lvl, associate,
        full_time, part_time, contract, temporary, volunteer, internship1, other,
        easy_apply,
        under10applicants,
        relevant, date_posted):
        
        base_url = 'https://www.linkedin.com/jobs/search/?'

        string_parts = [self.where(location),
                        self.keywords(keyword),
                        self.remote_filter(onsite, remote, hybrid),
                        self.date_posted_filter(anytime, past_month, past_week, past24hrs),
                        self.experience_filter(internship, entry_lvl, associate),
                        self.job_type_filter(full_time, part_time, contract, temporary, volunteer, internship1, other),
                        self.easy_apply_filter(easy_apply),
                        self.under_10_applicants_filter(under10applicants),
                        self.sort_by_search(relevant, date_posted)]

        string_parts = [i for i in string_parts if i]

        base_url +=  '&'.join(string_parts)

        return base_url