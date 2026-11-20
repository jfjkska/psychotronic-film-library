# Real index pages for the library: /director/<name>/, /country/<name>/,
# /decade/<1970s>/ and, once _data/genres.yml exists, /genre/<name>/.
#
# Each page lists its reviews as cards (newest film first) with a short
# introduction built only from the reviews' own front matter, a
# self-referencing canonical (from jekyll-seo-tag) and ItemList JSON-LD.
# Pages are made only where there are enough films to be worth a page;
# below that, links fall back to the existing anchors and homepage filters.
#
# The generator also publishes lookups in site.data["library_pages"] so
# templates can link a name to its page only when that page exists.
module PsychotronicLibrary
  THRESHOLDS = { "director" => 2, "country" => 3, "decade" => 2, "genre" => 4 }.freeze

  # "Antonio Margheriti (as Anthony M. Dawson)" -> "Antonio Margheriti";
  # "Gualtiero Jacopetti, Franco Prosperi" -> two people.
  def self.director_names(credit)
    credit.to_s.split(/\s*(?:,|&|\band\b)\s*/).map { |n| n.sub(/\s*\(as [^)]*\)\s*/i, "").strip }.reject(&:empty?)
  end

  def self.countries(value)
    value.to_s.split(%r{\s*[/,;]\s*}).map(&:strip).reject(&:empty?)
  end

  def self.decade(year)
    y = year.to_s.to_i
    y.positive? ? "#{y / 10 * 10}s" : nil
  end

  class IndexPage < Jekyll::PageWithoutAFile
    def initialize(site, kind, key, title, posts, extra = {})
      slug = kind == "decade" ? key : Jekyll::Utils.slugify(key, mode: "latin")
      super(site, site.source, File.join(kind, slug), "index.html")
      films = posts.sort_by { |p| [-p.data["year"].to_i, p.data["title"].to_s.downcase] }
      years = films.map { |p| p.data["year"].to_i }.select(&:positive?)
      data.merge!(
        "layout" => "listing",
        "title" => title,
        "kind" => kind,
        "key" => key,
        "films" => films,
        "film_count" => films.size,
        "first_year" => years.min,
        "last_year" => years.max,
        "body_class" => "listing-page"
      )
      data.merge!(extra)
      data["description"] ||= PsychotronicLibrary.describe(kind, key, films, years)
    end
  end

  def self.place(country)
    %w[UK USA].include?(country) ? "the #{country}" : country
  end

  def self.describe(kind, key, films, years)
    n = films.size
    span = if years.empty? then ""
           elsif years.min == years.max then ", from #{years.min}"
           else ", made between #{years.min} and #{years.max}"
           end
    case kind
    when "director" then "#{n} reviews of films directed by #{key}#{span}."
    when "country" then "#{n} reviews of films made in #{place(key)} (co-productions included)#{span.sub(', made between', ', from').sub(' and ', ' to ')}."
    when "decade" then "#{n} reviews of exploitation, horror and cult films made in the #{key}."
    else "#{n} reviews of #{key.downcase} films#{span}."
    end
  end

  class Generator < Jekyll::Generator
    safe true
    priority :high

    def generate(site)
      posts = site.posts.docs
      groups = Hash.new { |h, k| h[k] = Hash.new { |hh, kk| hh[kk] = [] } }
      posts.each do |post|
        PsychotronicLibrary.director_names(post.data["director"]).each { |n| groups["director"][n] << post }
        PsychotronicLibrary.countries(post.data["country"]).each { |c| groups["country"][c] << post }
        d = PsychotronicLibrary.decade(post.data["year"])
        groups["decade"][d] << post if d
      end

      genre_map = site.data["genres"]
      tag_to_genre = {}
      genre_intro = {}
      if genre_map.is_a?(Hash) && genre_map["genres"].is_a?(Array)
        genre_map["genres"].each do |g|
          name = g["name"].to_s
          genre_intro[name] = g["intro"]
          Array(g["tags"]).each { |t| tag_to_genre[t.to_s.downcase] = name }
        end
        posts.each do |post|
          Array(post.data["genres"]).map { |t| tag_to_genre[t.to_s.downcase] }.compact.uniq.each { |g| groups["genre"][g] << post }
        end
      end

      lookup = { "director" => {}, "country" => {}, "decade" => {}, "genre" => {}, "tag" => {} }
      titles = {
        "director" => ->(k) { "Films directed by #{k}" },
        "country" => ->(k) { "Films from #{PsychotronicLibrary.place(k)}" },
        "decade" => ->(k) { "Films of the #{k}" },
        "genre" => ->(k) { k }
      }
      groups.each do |kind, members|
        members.each do |key, list|
          next if list.size < THRESHOLDS[kind]
          extra = kind == "genre" && genre_intro[key] ? { "intro" => genre_intro[key] } : {}
          page = IndexPage.new(site, kind, key, titles[kind].call(key), list.uniq, extra)
          site.pages << page
          lookup[kind][key] = page.url
        end
      end
      tag_to_genre.each { |tag, genre| lookup["tag"][tag] = lookup["genre"][genre] if lookup["genre"][genre] }
      # Credited names ("X (as Y)") resolve to the person's page.
      posts.each do |post|
        credit = post.data["director"].to_s
        next if credit.empty? || lookup["director"].key?(credit)
        url = PsychotronicLibrary.director_names(credit).map { |n| lookup["director"][n] }.compact.first
        lookup["director"][credit] = url if url
      end
      site.data["library_pages"] = lookup
    end
  end
end
