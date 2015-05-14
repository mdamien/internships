class Internship < ActiveRecord::Base
  include Filterable

  scope :from_year, -> (year) { where("year >= ?", year) }
  scope :to_year, -> (year) { where("year <= ?", year) }
  scope :from_semester, -> (from_year, from_semester) { where.not("semester LIKE '%P%' and year = ?", from_year) unless from_semester == 'P' }
  scope :to_semester, -> (to_year, to_semester) { where.not("semester LIKE '%A%' and year = ?", to_year) unless to_semester == 'A' }
  scope :company_like, -> (company) { where("company LIKE ?", "%"+ company + "%") }
  scope :country_like, -> (country) { where("country LIKE ?", "%"+ country + "%") }
  scope :city_like, -> (city) { where("city LIKE ?", "%"+ city + "%") }
  scope :level_like, -> (level) { where("level_abbreviation LIKE ?", "%"+ level + "%") }
  scope :filiere_like, -> (filiere) { where("filiere_abbretiation LIKE ?", "%"+ filiere + "%") }
  scope :branch_like, -> (branch) { where("branch_abbreviation LIKE ?", "%"+ branch + "%") }
  scope :confidential_only, -> { where("confidential = 't'") }
  scope :exclude_not_done, -> { where("done = 't'") }
  scope :company_equal, -> (company) { where("company = ?", + company) }

  scope :order_by_semester_desc, -> { order(year: :DESC).order(semester: :ASC) }
  scope :order_by_semester_asc, -> { order(year: :ASC).order(semester: :DESC) }

  # from_s and to_s have to be "A2015" for instance.
  def self.from_semester_to_semester(from_s, to_s)
    from_year = from_s[1..4].to_i
    to_year = to_s[1..4].to_i
    from_semester = from_s[0]
    to_semester = to_s[0]

    return from_year(from_year)
               .to_year(to_year)
               .from_semester(from_year, from_semester)
               .to_semester(to_year, to_semester)
  end

  def self.order_internships_for_table
    return order(year: :DESC)
           .order(semester: :ASC)
           .order(country: :ASC)
           .order(company: :ASC)
  end

  def self.most_recent_internships
    most_recent_year = Internship.maximum("year")
    return Internship.from_year(most_recent_year)
  end

  def self.search query
    if query.has_key?(:from_semester) && query.has_key?(:to_semester)

      internships = from_semester_to_semester(query[:from_semester], query[:to_semester])
      internships = internships.confidential_only if query[:confidential_only].present?
      internships = internships.exclude_not_done unless query[:include_not_done].present?
      internships = internships.filter(query.slice(:company_like, :country_like, :city_like, :filiere_like, :done_only, :branch_like, :level_like))

      return internships
    end

    # Returning most recent internships if missing parameters.
    return most_recent_internships
  end

  def self.internship_count_by_semester query
    internships = search(query)

    internships = internships
                      .group("year")
                      .group("semester")
                      .group("branch_abbreviation")
                      .order_by_semester_asc
                      .count

    return internships
  end

  def self.all_internship_years
    return select(:year).distinct.order(year: :ASC)
  end

  def self.all_branches
    return select(:branch_abbreviation).where.not(branch_abbreviation: '').distinct.order(branch_abbreviation: :ASC)
  end

  def self.all_branches_for_select
    return self.all_branches.map { |b| b.branch_abbreviation }
  end

  def self.all_levels
    return select(:level_abbreviation).where.not(level_abbreviation: '').distinct.order(level_abbreviation: :ASC)
  end

  def self.all_levels_for_select
    return self.all_levels.map { |l| l.level_abbreviation }
  end

  def self.all_semesters_ordered
    semesters_in_database = select(:year).select(:semester).distinct.group("year").group("semester").order_by_semester_desc

    # Semesters will be sorted already, as we already sorted the data from the database.
    semesters = Array.new

    semesters_in_database.each do |s|
      semesters.push(s.semester + s.year.to_s)
    end

    return semesters
  end

  def self.all_countries_ordered_for_select
    return  select(:country).where("length(country) > 2").distinct.order(country: :ASC).map { |c| c.country }
  end

  def self.all_cities_grouped_by_country_for_select
    cities = select(:country)
        .select(:city)
        .where.not(city: '')
        .distinct
        .order(country: :ASC)
        .order(city: :ASC)

    cities_data = Hash.new

    cities.each do |c|
      if cities_data.has_key?(c.country)
        cities_data[c.country].push(c.city)
      else
        cities_data[c.country] = [c.city]
      end
    end

    return cities_data
  end

  def self.top_companies query
    internships = search(query)

    top_companies = internships.select(:company).group("company").order("count_company DESC").limit(20).count(:company)
    companies = top_companies.map { |c| c[0] }
    return internships.where(company: companies)
                     .group("year")
                     .group("semester")
                     .group("company")
                     .order_by_semester_asc
                     .count,
        top_companies
  end
end