package com.australiarecycling.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "suburbs")
public class Suburb {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String name;

  @Column(nullable = false, length = 10)
  private String postcode;

  @Column(nullable = false, length = 10)
  private String state;

  @ManyToOne(fetch = FetchType.LAZY)
  @JoinColumn(name = "council_id")
  private Council council;

  @Column(name = "created_at")
  private LocalDateTime createdAt;

  public Suburb() {}

  @PrePersist
  protected void onCreate() {
    createdAt = LocalDateTime.now();
  }

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getPostcode() {
    return postcode;
  }

  public void setPostcode(String postcode) {
    this.postcode = postcode;
  }

  public String getState() {
    return state;
  }

  public void setState(String state) {
    this.state = state;
  }

  public Council getCouncil() {
    return council;
  }

  public void setCouncil(Council council) {
    this.council = council;
  }

  public LocalDateTime getCreatedAt() {
    return createdAt;
  }

  public void setCreatedAt(LocalDateTime createdAt) {
    this.createdAt = createdAt;
  }
}
